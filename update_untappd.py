import requests
import os
from beer_search.models import BeerType


def update_item(beer_type):

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


def run():
    beer_types = BeerType.objects.all()
    for beer_type in beer_types:
        update_item(beer_type)