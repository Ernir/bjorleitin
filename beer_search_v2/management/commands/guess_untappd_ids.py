import os
import requests
from beer_search_v2.models import Product, AlcoholCategory, ContainerType, UntappdEntity
from beer_search_v2.utils import update_untappd_item
from django.core.management import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    def search_for_beer(self, search_string):
        url = "https://api.untappd.com/v4/search/beer"

        payload = {
            "client_id": os.environ.get("UNTAPPD_CLIENT"),
            "client_secret": os.environ.get("UNTAPPD_SECRET"),
            "q": search_string,
            "limit": 5
        }

        json_data = requests.get(url, params=payload).json()

        assert json_data["meta"]["code"] == 200

        found = json_data["response"]["beers"]["items"]
        return [item for item in found]

    def find_unknowns(self):
        return Product.objects.select_related(
                "product_type"
        ).filter(
                product_type__alcohol_category=AlcoholCategory.objects.get(name="beer")
        ).filter(
                product_type__untappd_info__isnull=True
        ).exclude(
                container=ContainerType.objects.get(name="Gjafaaskja")
        ).exclude(
                container=ContainerType.objects.get(name="Kútur")
        )

    def get_user_opinion(self, found):
        for i, item in enumerate(found):
            print("{}: {} ({}, {})".format(i, item["beer"]["beer_name"], item["beer"]["bid"],
                                           item["brewery"]["brewery_name"]))

        user_selected_beer = input("Enter the index of the correct beer, if any: ")
        try:
            index = int(user_selected_beer)
            return found[index]
        except (ValueError, IndexError):
            print("No appropriate index selected, continuing")

    def handle(self, *args, **options):
        unknown_beers = self.find_unknowns()

        if len(unknown_beers) > 50:
            print("Examining first 50 new beers")
            unknown_beers = unknown_beers[:50]

        for product in unknown_beers:
            product_type = product.product_type
            if product_type.untappd_info is None:
                found_items = self.search_for_beer(product_type.alias)
                if found_items:
                    print("Potential matches found for {}:".format(product_type.alias))
                    selected_item = self.get_user_opinion(found_items)
                    if selected_item is not None:
                        try:
                            new_untappd_entity = UntappdEntity.objects.create(untappd_id=selected_item["beer"]["bid"])
                        except IntegrityError:
                            new_untappd_entity = UntappdEntity.objects.get(untappd_id=selected_item["beer"]["bid"])
                        update_untappd_item(new_untappd_entity, True)
                        product_type.untappd_info = new_untappd_entity
                        product_type.save()
                else:
                    print("No matches found for {}.".format(product_type.alias))
