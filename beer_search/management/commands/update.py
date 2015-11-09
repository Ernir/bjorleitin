import json
import requests
import pytz
from datetime import datetime
from beer_search.models import Beer, Country, BeerType, \
    ContainerType, GiftBox
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    @classmethod
    def get_data(cls):
        """
        Steals beer data from the internal API of vinbudin.is.
        :return: A list of beers, as a JSON array. Format not particularly well defined.
        """
        domain = "http://www.vinbudin.is"
        location = "/addons/origo/module/ajaxwebservices/search.asmx/DoSearch"
        url = domain + location

        # Mandatory headers, as derived from website request info.
        headers = {
            "host": "www.vinbudin.is",
            "connection": "keep-alive",
            "cache-control": "max-age=0",
            "accept:": "application/json, text/javascript, */*; q=0.01",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Bjorleit/0.1 (+http://bjorleit.info/)",
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip, deflate, sdch",
            "accept-language": "en-GB,en;q=0.8,is;q=0.6,en-US;q=0.4",
        }

        # High values break the API.
        items_per_iteration = 100

        request_params = {
            "category": "beer",
            "skip": 0,
            "count": items_per_iteration,
            "orderBy": "name asc"
        }

        accumulated_list = []
        it_count = 0
        max_it = 10  # Safeguard, real stop is at bottom of loop.

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
            print("Fetched " + str(num_fetched) + " beers")

            if num_fetched > 0:
                accumulated_list.extend(data)
                # Moving on
                request_params["skip"] += items_per_iteration
            else:
                break

        return accumulated_list

    @classmethod
    def prepare_products_for_update(cls):
        # Marking all existing beers as not available until proven wrong.
        for beer in Beer.objects.all():
            beer.available = False
            beer.save()
        for box in GiftBox.objects.all():
            box.available = False
            box.save()

    @classmethod
    def clean_id(cls, atvr_id):
        """
        ATVR ids are strings of length 4, but the API returns an integer.
        The integers must be zero-padded and converted to strings for urls.
        """
        stringified_id = str(atvr_id)
        while len(stringified_id) < 5:
            stringified_id = "0" + stringified_id
        return stringified_id

    @staticmethod
    def get_or_create_country(country_name):
        try:
            country = Country.objects.get(name=country_name)
        except ObjectDoesNotExist:
            country = Country()
            country.name = country_name
            country.save()
        return country

    @classmethod
    def clean_date(cls, raw_date):
        """
        Converts the API's date format to a Python-friendly format.
        """
        first_seen_at = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S")
        return pytz.utc.localize(first_seen_at)

    @classmethod
    def update_beer_type(cls, beer, json_object):
        """
        Each beer product is just an instance of a particular type of beer,
        this common info is stored separately.
        """
        try:  # Checking if this beer belongs to a known type
            beer_type = BeerType.objects.get(name=beer.name)
            beer.beer_type = beer_type
        except ObjectDoesNotExist:  # Otherwise, create one
            beer_type = BeerType()
            beer_type.name = beer.name
            beer_type.abv = json_object["ProductAlchoholVolume"]
            country_name = json_object["ProductCountryOfOrigin"]
            beer_type.country = cls.get_or_create_country(country_name)
            beer_type.save()

            beer.beer_type = beer_type
            beer.save()

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
            raise ValueError("Gift boxes should be GiftBox instances.")
        else:
            container_type = ContainerType.objects.get(name="Ótilgreint")

        return container_type

    @classmethod
    def update_products(cls, product_list):

        for json_object in product_list:
            atvr_id = cls.clean_id(json_object["ProductID"])
            if not "ASKJA" in json_object["ProductContainerType"]:
                product = cls.get_beer_instance(json_object, atvr_id)
                raw_container = json_object["ProductContainerType"]
                product.container = cls.find_container_type(raw_container)
                cls.update_beer_type(product, json_object)
            else:
                product = cls.get_box_instance(json_object, atvr_id)

            product.available = True
            new_price = json_object["ProductPrice"]
            product.price = new_price  # We always update the price

            product.save()

    @classmethod
    def initialize_product(cls, product, json_object):
        print("New product created: " + json_object["ProductName"])
        product.name = json_object["ProductName"]
        product.volume = int(json_object["ProductBottledVolume"])
        product.first_seen_at = \
            cls.clean_date(json_object["ProductDateOnMarket"])
        product.temporary = json_object["ProductIsTemporaryOnSale"]
        return product

    @classmethod
    def get_box_instance(cls, json_object, atvr_id):
        try:  # Checking if we've found the box previously
            box = GiftBox.objects.get(atvr_id=atvr_id)
        except ObjectDoesNotExist:
            box = GiftBox()
            box.atvr_id = atvr_id
            box.abv = json_object["ProductAlchoholVolume"]
            country_name = json_object["ProductCountryOfOrigin"]
            box.country = cls.get_or_create_country(country_name)
            cls.initialize_product(box, json_object)
        return box

    @classmethod
    def get_beer_instance(cls, json_object, atvr_id):
        try:  # Checking if we've found the beer previously
            beer = Beer.objects.get(atvr_id=atvr_id)
        except ObjectDoesNotExist:
            beer = Beer()
            beer.atvr_id = atvr_id
            cls.initialize_product(beer, json_object)
        return beer

    def handle(self, *args, **options):
        try:
            beer_list = self.get_data()
        except ConnectionError:
            print("Unable to connect to vinbudin.is")
            beer_list = []

        if len(beer_list) > 0:
            self.prepare_products_for_update()
            self.update_products(beer_list)