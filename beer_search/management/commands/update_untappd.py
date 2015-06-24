import requests
import os
from beer_search.models import BeerType, ModifiableSettings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def update_item(self, beer_type):

        url = "https://api.untappd.com/v4/beer/info/" \
              + str(beer_type.untappd_id) \
              + "/"

        payload = {
            "client_id": os.environ.get("UNTAPPD_CLIENT"),
            "client_secret": os.environ.get("UNTAPPD_SECRET"),
            "compact": "true"
        }

        json_data = requests.get(url, params=payload).json()

        if json_data["meta"]["code"] == 200:
            old_rating = beer_type.untappd_rating
            new_rating = json_data["response"]["beer"]["rating_score"]
            beer_type.untappd_rating = new_rating
            beer_type.save()

            print(
                "Successfully updated "
                + beer_type.name
                + " from "
                + str(old_rating)
                + " to "
                + str(new_rating)
            )

    def get_indices(self):
        """

        The untappd API is rate limited, the list needs to be limited as well.
        """
        mod_settings = ModifiableSettings.objects

        start_index_setting = mod_settings.get(key="untappd_start_index")
        num_per_run_setting = mod_settings.get(key="untappd_items_per_run")

        start_index = start_index_setting.value
        end_index = start_index_setting.value + num_per_run_setting.value

        return start_index, end_index

    def update_indices(self, end_index):
        mod_settings = ModifiableSettings.objects
        start_index_setting = mod_settings.get(key="untappd_start_index")

        num_items = BeerType.objects.filter(untappd_id__isnull=False).count()

        if end_index > num_items:  # We've finished the list for now, resetting
            start_index_setting.value = 0
        else:  # Next time, we start further into the list.
            start_index_setting.value = end_index

        start_index_setting.save()

    def handle(self, *args, **options):
        beer_types = BeerType.objects.filter(untappd_id__isnull=False).all()
        start_index, end_index = self.get_indices()
        for beer_type in beer_types[start_index:end_index]:
            self.update_item(beer_type)
        self.update_indices(end_index)