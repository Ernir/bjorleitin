from django.core.exceptions import ObjectDoesNotExist
import os
import requests
from beer_search_v2.models import Brewery, UntappdStyle, Product, Country, AlcoholCategory, ContainerType


def update_untappd_item(untappd_entity, verbose=True):
    url = "https://api.untappd.com/v4/beer/info/{0}/".format(untappd_entity.untappd_id)

    payload = {
        "client_id": os.environ.get("UNTAPPD_CLIENT"),
        "client_secret": os.environ.get("UNTAPPD_SECRET"),
        "compact": "true"
    }

    json_data = requests.get(url, params=payload).json()

    assert json_data["meta"]["code"] == 200

    old_rating = untappd_entity.rating
    new_rating = json_data["response"]["beer"]["rating_score"]
    untappd_entity.rating = new_rating

    if untappd_entity.style is None:
        style_name = json_data["response"]["beer"]["beer_style"]
        style = get_untappd_style_instance(style_name)
        untappd_entity.style = style
        if verbose:
            print("Added style {0} to {1}.".format(style_name, untappd_entity.name))

    if untappd_entity.brewery is None:
        untappd_id = json_data["response"]["beer"]["brewery"]["brewery_id"]
        untappd_name = json_data["response"]["beer"]["brewery"]["brewery_name"]
        brewery = get_brewery_instance(untappd_id, untappd_name)
        untappd_entity.brewery = brewery
        if verbose:
            print("Added brewery {0} to {1}.".format(untappd_name, untappd_entity.name))

    untappd_entity.save()

    if verbose:
        print("Successfully updated {0} from {1} to {2}".format(untappd_entity.name, old_rating, new_rating))


def get_untappd_style_instance(style_name, verbose=True):
    try:
        style = UntappdStyle.objects.get(name=style_name)
    except ObjectDoesNotExist:
        style = UntappdStyle()
        style.name = style_name
        style.save()
        if verbose:
            print("Created new style: {0}".format(style_name))
    return style


def get_brewery_instance(untappd_id, brewery_name, verbose=True):
    try:
        brewery = Brewery.objects.get(untappd_id=untappd_id)
    except ObjectDoesNotExist:
        brewery = Brewery()
        brewery.untappd_id = untappd_id
        brewery.name = brewery_name
        brewery.save()
        if verbose:
            print("Created new brewery: {0}".format(brewery_name))
    return brewery


def get_country_instance(country_name):
    try:
        country = Country.objects.get(name__iexact=country_name)
    except ObjectDoesNotExist:
        country = Country()
        country.name = country_name
        country.save()
    return country


def get_alcohol_category_instance(cat_name):
    try:
        category = AlcoholCategory.objects.get(name=cat_name)
    except ObjectDoesNotExist:
        category = AlcoholCategory()
        category.name = cat_name
        category.save()
    return category


def get_container_instance(container_name):
    try:
        container = ContainerType.objects.get(name=container_name)
    except ObjectDoesNotExist:
        container = ContainerType()
        container.name = container_name
        container.save()
    return container
