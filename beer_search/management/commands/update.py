import json
from beer_search.models import Beer, Country, Store, BeerType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    @staticmethod
    def read_file(path):
        with open(path) as data_file:
            products = json.load(data_file)

        beers = []  # We don't care about other products.

        for product in products:
            if "category" in product:
                atvr_beercategories = ["Lagerbjór", "Öl", "Aðrar bjórtegundir"]
                if product["category"] in atvr_beercategories:
                    beers.append(product)

        return beers

    @staticmethod
    def parse_price(price_string):
        price_string = price_string.replace("kr", "").replace(".", "")
        return int(price_string.strip())

    @staticmethod
    def parse_abv(abv_string):
        return float(abv_string.replace(",", "."))

    @staticmethod
    def parse_volume(volume_string):
        if "L" in volume_string:
            volume_string = volume_string.replace("L", "").replace(",", ".")
            volume = int(float(volume_string.strip())*1000)
        else:
            volume_string = volume_string.replace("ml", "")
            volume = int(volume_string.strip())
        return volume

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
    def update_beers(cls, beer_list, reset_new_status):

        # Marking all preexisting beers as not available until proven wrong.
        # If reset_new_status == True, all beers are also set as not_new.
        for beer in Beer.objects.all():
            beer.available = False
            if reset_new_status:
                beer.new = False
            beer.save()

        for store in Store.objects.all():
            for beer_assignment in store.beers_available.all():
                store.beers_available.remove(beer_assignment)

        for beer_json_object in beer_list:
            try:  # Checking if we've found the beer previously
                atvr_id = beer_json_object["id"]
                beer = Beer.objects.get(atvr_id=atvr_id)
                beer.available = True
            except ObjectDoesNotExist:  # Else, we initialize it
                beer = Beer()
                beer.atvr_id = beer_json_object["id"]
                beer.name = beer_json_object["title"]
                beer.abv = cls.parse_abv(beer_json_object["abv"])
                # Some version mismatches here
                if "volume" in beer_json_object:
                    beer.volume = cls.parse_volume(beer_json_object["volume"])
                elif "weight" in beer_json_object:
                    beer.volume = cls.parse_volume(beer_json_object["weight"])
                else:
                    beer.volume = 0

                country_name = beer_json_object["country"]
                beer.country = cls.get_or_create_country(country_name)

                print("New beer created: " + beer_json_object["title"])

            new_price = cls.parse_price(beer_json_object["price"])
            beer.price = new_price  # We always update the price

            try:  # Checking if this beer belongs to a known type
                beer_type = BeerType.objects.get(name=beer.name)
                beer.beer_type = beer_type
            except ObjectDoesNotExist:  # Otherwise, create one
                if not "Ýmsir" in beer.style.name:  # ... unless it's a box.
                    beer_type = BeerType()
                    beer_type.name = beer.name
                    beer_type.abv = beer.abv
                    beer_type.style = beer.style
                    beer_type.country = beer.country
                    beer_type.save()
                    beer.beer_type = beer_type

            beer.save()

            # Populating the store information. First, we go deep...
            for region_dict in beer_json_object["availability"]:
                for store_dict in region_dict["stores"]:
                    store_ref = store_dict["store"]
                    # ... then we attempt to update the store's beer list.
                    try:
                        if store_ref != " ":  # There are odd blanks sometimes
                            store = Store.objects.\
                                get(reference_name=store_ref)
                            store.beers_available.add(beer)
                            store.save()
                    except ObjectDoesNotExist:
                        print("Store reference " + store_ref + " not found.")

    def handle(self, *args, **options):
        file_in = "products-metadata.json"
        reset_new_status=False

        beer_list = self.read_file(file_in)
        self.update_beers(beer_list, reset_new_status)