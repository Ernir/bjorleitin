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
        """

        :param searchstring: A string that will be sent to Ratebeer as a search term
        :param beername: The beer's name as defined by the beer search, used for comparison
        :param breweryname: The brewery name, as defined by the beer search, used for comparison
        :return: A list of search query results
        """
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
        """
        Iteratively calls post_to_ratebeer to try to find the
        """

        # First try with just the beer name
        found_beers = cls.post_to_ratebeer(beer_name, beer_name, "")
        if 0 < len(found_beers) < 20:  # Very many or no results are not acceptable
            return found_beers

        # Then, try including the brewery name, and chopping out words
        search_components = "{} {}".format(beer_name, brewery_name).strip().split()
        print("Looking for {}".format(" ".join(search_components)))
        chopped_words = 0
        while chopped_words < len(search_components) and not found_beers:
            search_string = " ".join(search_components[:len(search_components) - chopped_words])
            found_beers = cls.post_to_ratebeer(search_string, beer_name, brewery_name)
            chopped_words += 1
        if not found_beers:
            print("Found nothing for {}".format(" ".join(search_components)))
        return found_beers

    def add_arguments(self, parser):
        parser.add_argument("start_index", type=int, default=0)

    def handle(self, *args, **options):
        print("Finding relevant products")
        beers = ProductType.objects.filter(ratebeer_info__isnull=True, untappd_info__isnull=False).all()
        beers = beers[options["start_index"]:]
        for beer in beers:
            found_beers = self.perform_searches(beer.alias, beer.untappd_info.brewery.alias)
            if found_beers:
                found_beers = found_beers[:20]
                rb = sorted(found_beers, key=lambda found: found["lev"])  # Find best match according to lev
                user_input = ""
                while user_input.lower() not in ["n", "break"]:
                    if len(rb) > 1:
                        for i, rb_info in enumerate(found_beers):
                            print("{}: {}".format(i, rb_info["rbname"]))
                        user_input = input("Does this look right to you? (<number>/n/break): ")
                        try:
                            user_input = int(user_input)
                        except ValueError:
                            pass
                    else:
                        print("Precisely one result, assuming correctness")
                        user_input = 0
                    if user_input in list(range(0, len(found_beers))):
                        rb = rb[user_input]
                        beer.ratebeer_info = RatebeerEntity.objects.create(
                                ratebeer_id=rb["rbid"],
                                name=rb["rbname"],
                                score=rb["rbscore"],
                                number_of_ratings=rb["rbratings"],
                                levenshtein_confidence=rb["lev"]
                        )
                        beer.save()
                        break
                if user_input == "break":
                    print("Stopping")
                    break
