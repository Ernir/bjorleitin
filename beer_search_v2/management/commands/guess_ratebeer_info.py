import re
import requests
from beer_search_v2.models import ProductType, RatebeerEntity
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

"""
This module is largely taken from Hrafnkell! Send all your firstborns to him.
https://github.com/hrafnkell/jg/blob/master/ratebeer.py
"""


class Command(BaseCommand):
    @classmethod
    def levenshtein(cls, a, b):
        "Calculates the Levenshtein distance between a and b."
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a, b = b, a
            n, m = m, n

        current = range(n + 1)
        for i in range(1, m + 1):
            previous, current = current, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete = previous[j] + 1, current[j - 1] + 1
                change = previous[j - 1]
                if a[j - 1] != b[i - 1]:
                    change = change + 1
                current[j] = min(add, delete, change)

        return current[n]

    @classmethod
    def post_to_ratebeer(cls, searchstring, beername, breweryname):
        r = requests.post('http://www.ratebeer.com/findbeer.asp', data={'BeerName': searchstring})
        soup = BeautifulSoup(r.text, 'html5lib')
        rb = soup.find_all('a', class_='rate')
        beers = []
        # Build collection of results
        for b in rb:
            rbid = re.findall('(\d+)', b['href'])[0]
            rbname = b.parent.previous_sibling('a')[0].text.strip()
            rbscore = b.parent.next_sibling.next_sibling.text.strip() or 0
            rbratings = b.parent.next_sibling.next_sibling.next_sibling.text.strip()
            lev = cls.levenshtein(rbname, "%s %s" % (breweryname, beername))
            beers.append({
                "rbid": int(rbid),
                "rbname": rbname,
                "rbscore": int(rbscore),
                "rbratings": int(rbratings),
                "lev": lev
            })
        return beers

    @classmethod
    def perform_searches(cls, beer_name, brewery_name):
        search_components = "{} {}".format(beer_name, brewery_name).strip().split()
        print("Looking for {}".format(" ".join(search_components)))
        found_beers = []
        chopped_words = 0
        while chopped_words < len(search_components) and not found_beers:
            search_string = " ".join(search_components[:len(search_components) - chopped_words])
            found_beers = cls.post_to_ratebeer(search_string, beer_name, brewery_name)
            chopped_words += 1
        else:
            if chopped_words > 0:
                print("Match found by chopping off {} words.".format(chopped_words))
        if not found_beers:
            print("Found nothing for {}".format(" ".join(search_components)))
        return found_beers

    def handle(self, *args, **options):
        print("Finding relevant products")
        beers = [
            product for product in ProductType.objects.filter(ratebeer_info__isnull=True).all() if product.is_relevant
            ]  # No DB-filtering by property
        for beer in beers:
            if beer.untappd_info:
                brewery_name = beer.untappd_info.brewery.alias
            else:
                brewery_name = ""

            found_beers = self.perform_searches(beer.alias, brewery_name)

            if found_beers:
                rb = sorted(found_beers, key=lambda found: found["lev"])[0]  # Find best match according to lev
                user_input = ""
                while user_input.lower() not in ["y", "n", "break"]:
                    user_input = input(
                            "Best match is {}. Does this look right to you? (y/n/break): ".format(rb["rbname"])
                    )
                    if user_input == "y":
                        beer.ratebeer_info = RatebeerEntity.objects.create(
                                ratebeer_id=rb["rbid"],
                                name=rb["rbname"],
                                score=rb["rbscore"],
                                number_of_ratings=rb["rbratings"],
                                levenshtein_confidence=rb["lev"]
                        )
                        beer.save()
                if user_input == "break":
                    print("Stopping")
                    break
