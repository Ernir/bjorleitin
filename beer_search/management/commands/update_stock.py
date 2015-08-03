import requests
from bs4 import BeautifulSoup
from beer_search.models import Beer, Store
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def get_beer_data(self, atvr_id):
        """
        :param atvr_id: The ID of one of ATVR's beers.
        :return: A dictionary consisting of store names as keys, and the
        stock status of the beer with the given ID as values.
        """
        base_url = "http://www.vinbudin.is/DesktopDefault.aspx/tabid-54"
        params = {"productID": atvr_id}
        try:
            html_doc = requests.get(base_url, params=params).text
        except ConnectionError:
            print("Could not establish a connection to ATVR.")
            # Defaults to an undefined stock
            return None

        soup = BeautifulSoup(html_doc, 'html.parser')
        stock_status = soup.find(id="div-stock-status")
        store_names = stock_status.find_all(class_="store")

        info = {}
        for store in store_names:
            info[store.string] = int(store.next_sibling.string)

        return info

    def update_beer_by_id(self, atvr_id, stock_info):
        """

        Updates the stock status of the beer with the given id with the
        info given by stock_info. Stock info is of a format as specified by
        the function get_beer_data().
        """


        beer = Beer.objects.get(atvr_id=atvr_id)
        # An empty stock is OK, an undefined one isn't.
        if stock_info is None:
            print("No data received for " + beer.name + ", no update.")
            return
        beer.store_set.clear()
        beer.save()

        for store_reference in stock_info:
            store = Store.objects.get(reference_name=store_reference)
            store.beers_available.add(beer)
            store.save()

    def handle(self, *args, **options):
        queryset = Beer.available_beers.values_list("atvr_id", flat=True)
        for atvr_id in queryset:
            stock_info = self.get_beer_data(atvr_id)
            self.update_beer_by_id(atvr_id, stock_info)