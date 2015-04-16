import csv
from beer_search.models import Beer
from django.core.exceptions import ObjectDoesNotExist


def clean_csv(input_filename, output_filename):
    raw_file = open(input_filename, "r")
    cleaned_file = open(output_filename, 'w+')

    is_odd = True  # The file comes with messed up newlines.
    next(raw_file)  # skipping the header
    for line in raw_file:
        line = line.replace("                                    ", "")
        if is_odd:
            last = line
        else:
            newline = last + line  # Goes to hell if is_odd = False on init
            newline = newline.replace("\n", "\",\"", 1)
            cleaned_file.write(newline)
        is_odd = not is_odd


def parse_csv(filename):
    file = open(filename, "r")
    beer_reader = csv.reader(file, delimiter=",")
    beer_list = []
    for row in beer_reader:
        beer = {"name": row[0]}

        beer["id"] = row[1][1:-1]  # The id is surrounded by parentheses

        if "L" in row[2]:  # Some beers are in L, others in mL
            # Cleanup, standardizing to mL
            raw_volume = row[2][:-2].replace(",", ".")
            volume = int(float(raw_volume)*1000)
        else:
            raw_volume = row[2][:-2].strip(" ")
            volume = int(raw_volume)
        beer["volume"] = volume

        # Storing ABV: strip off the % sign,
        beer["abv"] = float(row[3][:-1].replace(",", "."))

        # Stripping out the Icelandic thousand markers and ISK unit.
        beer["price"] = int(row[4][:-3].replace(".", ""))

        beer_list.append(beer)

    return beer_list


def update_beers(beer_list):

    # Marking all preexisting beers as not-new, and not available
    # until proven otherwise.
    for beer in Beer.objects.all():
        beer.new = False
        beer.available = False
        beer.save()

    for beer_dict in beer_list:
        already_exists = False
        try:  # Checking if we've found the beer previously
            atvr_id = beer_dict["id"]
            beer = Beer.objects.get(atvr_id=atvr_id)
            beer.available = True
            already_exists = True
        except ObjectDoesNotExist:  # Else, we initialize it
            beer = Beer()

        beer.price = beer_dict["price"]  # We always update the price
        if not already_exists:
            beer.atvr_id = beer_dict["id"]
            beer.name = beer_dict["name"]
            beer.abv = beer_dict["abv"]
            beer.volume = beer_dict["volume"]

        beer.save()


def run():
    file_in = "atvr.csv"
    file_clean = "atvr_clean.csv"

    clean_csv(file_in, file_clean)
    beer_dict = parse_csv(file_clean)
    update_beers(beer_dict)