from django.core.exceptions import ObjectDoesNotExist
import os
import requests
from beer_search_v2.models import Brewery, UntappdStyle, Country, AlcoholCategory, ContainerType, Product
from collections import OrderedDict


def get_main_display():
    """

    Returns a list of dictionaries containing the information needed to display and filter
    the main table on the index page.
    """

    # First we gather the requisite information
    beer = AlcoholCategory.objects.get(name="beer")
    gift_box = get_container_instance("Gjafaaskja")
    products = Product.objects.select_related(
            "container",
            "product_type",
            "product_type__country",
            "product_type__alcohol_category",
            "product_type__untappd_info",
            "product_type__untappd_info__brewery",
            "product_type__untappd_info__style__simplifies_to"
    ).filter(
        product_type__alcohol_category=beer,
        available=True
    ).exclude(
        container=gift_box
    ).order_by("product_type__alias")

    # Then we curate it
    type_dict = OrderedDict()
    for product in products.all():
        pid = product.product_type_id
        if pid not in type_dict:  # Initialize with all data common among all products of the same type
            type_dict[pid] = {
                "name": str(product.product_type),
                "productId": pid,
                "containers": [product.container.name],
                "abv": product.product_type.abv,
                "minVolume": product.volume,
                "maxVolume": product.volume,
                "minPrice": product.price,
                "maxPrice": product.price
            }

            if product.product_type.country:
                type_dict[pid]["country"] = product.product_type.country.name

            if product.product_type.untappd_info:
                u_info = product.product_type.untappd_info
                if u_info.style and u_info.style.simplifies_to:
                    type_dict[pid]["style"] = u_info.style.simplifies_to.name
                if u_info.brewery:
                    type_dict[pid]["brewery"] = str(u_info.brewery)
                    if "country" not in type_dict[pid]:  # Country info is shaky, stored with great redundancy
                        if u_info.brewery.country:
                            type_dict[pid]["country"] = u_info.brewery.country.name
                        elif u_info.brewery.country_name:
                            type_dict[pid]["country"] = u_info.brewery.country_name
                if u_info.rating:
                    type_dict[pid]["untappdRating"] = u_info.rating
            # Fillers for those entries with no known information
            if "country" not in type_dict[pid]:
                type_dict[pid]["country"] = "?"
            if "brewery" not in type_dict[pid]:
                type_dict[pid]["brewery"] = "?"
            if "style" not in type_dict[pid]:
                type_dict[pid]["style"] = "?"
        else:
            type_dict[pid]["maxVolume"] = max(type_dict[pid]["maxVolume"], product.volume)
            type_dict[pid]["minVolume"] = min(type_dict[pid]["minVolume"], product.volume)
            type_dict[pid]["maxPrice"] = max(type_dict[pid]["maxPrice"], product.price)
            type_dict[pid]["minPrice"] = min(type_dict[pid]["minPrice"], product.price)
            if product.container.name not in type_dict[pid]["containers"]:
                type_dict[pid]["containers"].append(product.container.name)

    return [item for item in type_dict.values()]


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
            print("Added style {0} to {1}.".format(style_name, untappd_entity.product_name))

    if untappd_entity.brewery is None:
        untappd_id = json_data["response"]["beer"]["brewery"]["brewery_id"]
        untappd_name = json_data["response"]["beer"]["brewery"]["brewery_name"]
        country_name = json_data["response"]["beer"]["brewery"]["country_name"]
        brewery = get_brewery_instance(untappd_id, untappd_name, country_name)
        untappd_entity.brewery = brewery
        if verbose:
            print("Added brewery {0} to {1}.".format(untappd_name, untappd_entity.product_name))

    untappd_entity.save()

    if verbose:
        print("Successfully updated {0} from {1} to {2}".format(untappd_entity.product_name, old_rating, new_rating))


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


def get_brewery_instance(untappd_id, brewery_name, brewery_country, verbose=True):
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
