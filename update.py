import json
from beer_search.models import Beer, Country, Store
from django.core.exceptions import ObjectDoesNotExist


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


def parse_price(price_string):
    price_string = price_string.replace("kr", "").replace(".", "")
    return int(price_string.strip())


def parse_abv(abv_string):
    return float(abv_string.replace(",", "."))


def parse_volume(volume_string):
    if "L" in volume_string:
        volume_string = volume_string.replace("L", "").replace(",", ".")
        volume = int(float(volume_string.strip())*1000)
    else:
        volume_string = volume_string.replace("ml", "")
        volume = int(volume_string.strip())
    return volume


def get_or_create_country(country_name):
    try:
        country = Country.objects.get(name=country_name)
    except ObjectDoesNotExist:
        country = Country()
        country.name = country_name
        country.save()
    return country


def update_beers(beer_list, reset_new_status):

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
            beer.abv = parse_abv(beer_json_object["abv"])
            # Some version mismatches here
            if "volume" in beer_json_object:
                beer.volume = parse_volume(beer_json_object["volume"])
            elif "weight" in beer_json_object:
                beer.volume = parse_volume(beer_json_object["weight"])
            else:
                beer.volume = 0

            country_name = beer_json_object["country"]
            beer.country = get_or_create_country(country_name)
            
            print("New beer created: " + beer_json_object["title"])

        new_price = parse_price(beer_json_object["price"])
        beer.price = new_price  # We always update the price

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


def run(reset_new_status=False):
    file_in = "products-metadata.json"

    beer_list = read_file(file_in)
    update_beers(beer_list, reset_new_status)