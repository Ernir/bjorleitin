import json
import requests
import pytz
from datetime import datetime
from beer_search_v2.models import Product, ProductType, ContainerType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from beer_search_v2.utils import get_country_instance, get_alcohol_category_instance, renew_cache


class Command(BaseCommand):
    @classmethod
    def get_data(cls, verbose=True):
        """
        Steals product data from the internal API of vinbudin.is.
        :return: A list of products, as a JSON array. Format not particularly well defined.
        """
        domain = "http://www.vinbudin.is"
        location = "/addons/origo/module/ajaxwebservices/search.asmx/DoSearch"
        url = domain + location

        # Mandatory headers, as derived from website request info.
        headers = {
            "host": "www.vinbudin.is",
            "connection": "keep-alive",
            "cache-control": "max-age=0",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Bjorleit/0.2 (+http://bjorleit.info/)",
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip, deflate, sdch",
            "accept-language": "en-GB,en;q=0.8,is;q=0.6,en-US;q=0.4",
        }

        # High values break the API.
        items_per_iteration = 100

        request_params = {
            "category": "beer",  # This whole k-v pair can be omitted, to search all products
            "skip": 0,
            "count": items_per_iteration,
            "orderBy": "name asc"
        }

        accumulated_list = []
        it_count = 0
        max_it = 100  # Safeguard, real stop is at bottom of loop.

        while it_count <= max_it:
            it_count += 1

            json_response = requests.get(
                    url,
                    headers=headers,
                    params=request_params
            ).json()

            # The whole thing is apparently a string inside a JSONObject.
            data = json.loads(json_response["d"])
            data = data["data"]  # Nesting fun

            num_fetched = len(data)
            if verbose:
                print("Fetched " + str(num_fetched) + " products")

            if num_fetched > 0:
                accumulated_list.extend(data)
                # Moving on
                request_params["skip"] += items_per_iteration
            else:
                break

        return accumulated_list

    @classmethod
    def prepare_products_for_update(cls):
        # Marking all existing products from ÁTVR as not available until proven wrong.
        for product in Product.objects.filter(atvr_id__isnull=False).all():
            product.available_in_atvr = False
            product.save()

    @classmethod
    def clean_atvr_id(cls, atvr_id):
        """
        ATVR ids are strings, but the API returns an integer.
        The integers must be zero-padded and converted to strings for urls.
        """
        stringified_id = str(atvr_id)
        while len(stringified_id) < 5:
            stringified_id = "0" + stringified_id
        return stringified_id

    @classmethod
    def clean_date(cls, raw_date):
        """
        Converts the API's date format to a Python-friendly format.
        """
        first_seen_at = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S")
        return pytz.utc.localize(first_seen_at)

    @classmethod
    def update_product_type(cls, product, json_object):
        """
        Each product is an instance of a particular product type, this common info is stored separately.
        """

        if not product.product_type_id:
            product_type = ProductType()
            product_type.name = product.name
            product_type.abv = json_object["ProductAlchoholVolume"]
            product_type.country = get_country_instance(json_object["ProductCountryOfOrigin"])
            product_type.alcohol_category = get_alcohol_category_instance(json_object["ProductCategory"]["name"])
            product_type.save()

            product.product_type = product_type
            print("Creating new product type: {0}".format(product_type.name))
            product.save()

    @classmethod
    def find_container_type(cls, atvr_name):
        """
        The ATVR database contains container info with non-human-friendly
        names. This function finds the appropriate Bjórleit Container type.
        """

        if atvr_name == "FL.":
            container_type = ContainerType.objects.get(name="Flaska")
        elif atvr_name == "DS.":
            container_type = ContainerType.objects.get(name="Dós")
        elif atvr_name == "KÚT.":
            container_type = ContainerType.objects.get(name="Kútur")
        elif "ASKJA" in atvr_name:
            container_type = ContainerType.objects.get(name="Gjafaaskja")
        else:
            container_type = ContainerType.objects.get(name="Ótilgreint")

        return container_type

    @classmethod
    def update_products(cls, product_list):

        for json_object in product_list:
            product_id = cls.clean_atvr_id(json_object["ProductID"])
            product = cls.get_product_instance(json_object, product_id)
            if not product.container_id:
                raw_container_name = json_object["ProductContainerType"]
                product.container = cls.find_container_type(raw_container_name)
            cls.update_product_type(product, json_object)
            product.available_in_atvr = True
            product.price = json_object["ProductPrice"]  # We always update the price

            product.save()

    @classmethod
    def get_product_instance(cls, json_object, atvr_id):
        try:  # Checking if we've found the product previously
            product = Product.objects.get(atvr_id=atvr_id)
        except ObjectDoesNotExist:
            product = Product()
            product.atvr_id = atvr_id
            cls.initialize_product(product, json_object)
        return product

    @classmethod
    def initialize_product(cls, product, json_object):
        print("New product created: " + json_object["ProductName"])
        product.name = json_object["ProductName"]
        product.price = json_object["ProductPrice"]
        product.volume = int(json_object["ProductBottledVolume"])
        product.first_seen_at = cls.clean_date(json_object["ProductDateOnMarket"])
        product.temporary = json_object["ProductIsTemporaryOnSale"]
        return product

    def handle(self, *args, **options):
        try:
            product_list = self.get_data(verbose=True)
        except ConnectionError:
            print("Unable to connect to vinbudin.is")
            product_list = []

        if len(product_list) > 0:
            self.prepare_products_for_update()
            self.update_products(product_list)

        for product_type in ProductType.objects.filter().all():
            product_type.update_availability(verbose=False)

        renew_cache()
