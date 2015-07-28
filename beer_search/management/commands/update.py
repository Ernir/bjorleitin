import json
import requests
from beer_search.models import Beer, Country, Store, BeerType, \
    ContainerType
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

            if len(data) > 0:
                accumulated_list.extend(data)
                # Moving on
                request_params["skip"] += items_per_iteration
            else:
                break

        return accumulated_list

    @classmethod
    def prepare_beers_for_update(cls, reset_new_status):
        # Marking all existing beers as not available until proven wrong.
        # If reset_new_status == True, all beers are also set as not_new.
        for beer in Beer.objects.all():
            beer.available = False
            if reset_new_status:
                beer.new = False
            beer.save()

    @classmethod
    def clean_id(cls, atvr_id):
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
    def update_beer_type(cls, beer, json_object):
        try:  # Checking if this beer belongs to a known type
            beer_type = BeerType.objects.get(name=beer.name)
            beer.beer_type = beer_type
        except ObjectDoesNotExist:  # Otherwise, create one
            if not "ASKJA" in json_object["ProductContainerType"]:  # ... unless it's a box.
                beer_type = BeerType()
                beer_type.name = beer.name
                beer_type.abv = beer.abv
                beer_type.style = beer.style
                beer_type.country = beer.country
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
        elif "ASKJA" in atvr_name:
            container_type = ContainerType.objects.get(name="Gjafaaskja")
        elif atvr_name == "KÚT.":
            container_type = ContainerType.objects.get(name="Kútur")
        else:
            container_type = ContainerType.objects.get(name="Ótilgreint")

        return container_type

    @classmethod
    def update_availability_info(cls):
        pass  # ToDo: Implement

    @classmethod
    def update_products(cls, product_list):

        for json_object in product_list:
            atvr_id = cls.clean_id(json_object["ProductID"])
            try:  # Checking if we've found the beer previously
                beer = Beer.objects.get(atvr_id=atvr_id)
                beer.available = True
            except ObjectDoesNotExist:  # Else, we initialize it
                beer = Beer()
                beer.atvr_id = atvr_id
                beer.name = json_object["ProductName"]
                beer.abv = json_object["ProductAlchoholVolume"]
                beer.volume = int(json_object["ProductBottledVolume"])
                beer.container = cls.find_container_type(json_object["ProductContainerType"])

                country_name = json_object["ProductCountryOfOrigin"]
                beer.country = cls.get_or_create_country(country_name)

                print("New beer created: " + json_object["ProductName"])

            new_price = json_object["ProductPrice"]
            beer.price = new_price  # We always update the price

            # Significant updates done in their own functions
            cls.update_beer_type(beer, json_object)
            cls.update_availability_info()

            beer.save()

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument('--clearall',
            dest="clearall",
            default=False,
            help='Sets all beers as "not new".'
        )

    def handle(self, *args, **options):
        try:
            beer_list = self.get_data()
        except ConnectionError:
            print("Unable to connect to vinbudin.is")
            beer_list = []

        if len(beer_list) > 0:
            if options["clearall"]:
                set_as_not_new = False
            else:
                set_as_not_new = True
            self.prepare_beers_for_update(set_as_not_new)
            self.update_products(beer_list)