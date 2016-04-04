import requests
from bs4 import BeautifulSoup
from beer_search_v2.models import Product
from django.core.management.base import BaseCommand
from pprint import PrettyPrinter


class Command(BaseCommand):

    def get_product_stock(self, atvr_id):
        """
        :param atvr_id: The ID of one of ATVR's products.
        :return: A dictionary consisting of store names as keys, and the
        stock status of the given product as values.
        """

        base_url = "http://www.vinbudin.is/Heim/v%C3%B6rur/stoek-vara.aspx/"
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

    def update_product_by_id(self, atvr_id, stock_info):
        """

        Updates the stock status of the beer with the given id with the
        info given by stock_info. Stock info is of a format as specified by
        the function get_beer_data().
        """

        product = Product.objects.get(atvr_id=atvr_id)
        # An empty stock is OK, an undefined one isn't.
        if stock_info is None:
            print("No data received for " + product.name + ", no update.")
            return
        product.store_set.clear()
        product.save()

        for store_reference in stock_info:
            store = Store.objects.get(reference_name=store_reference)
            store.beers_available.add(product)
            store.save()

    def handle(self, *args, **options):
        beers = Beer.objects.available_beers().filter(name="Amstel")
        pp = PrettyPrinter()
        for beer in beers:
            stock_info = self.get_product_stock(beer.atvr_id)
            pp.pprint(stock_info)
            #self.update_beer_by_id(beer.atvr_id, stock_info)
