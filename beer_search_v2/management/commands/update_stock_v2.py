import requests
from beer_search_v2.utils import renew_cache
from bs4 import BeautifulSoup
from beer_search_v2.models import Product
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def get_product_data(self, atvr_id):
        """
        :param atvr_id: The ID of one of ATVR's products.
        :return: A dictionary consisting of store names as keys, and the
        stock status of the product with the given ID as values.
        """

        base_url = "http://www.vinbudin.is/Heim/v%C3%B6rur/stoek-vara.aspx/"
        params = {"productID": atvr_id}
        try:
            html_doc = requests.get(base_url, params=params).text
        except ConnectionError:
            print("Could not establish a connection to ATVR for product {}".format(atvr_id))
            # Defaults to an empty stock
            return []

        soup = BeautifulSoup(html_doc, 'html.parser')
        stock_status = soup.find(id="div-stock-status")
        if stock_status:
            store_names = stock_status.find_all(class_="store")
        else:
            return []  # If the div can't be found, assume the stock is empty.

        info = []
        for store in store_names:
            info.append({"store": store.string, "stock": int(store.next_sibling.string)})
        return info

    def handle(self, *args, **options):
        verbose = True
        products = Product.objects.all()
        for product in products:
            stock_info = self.get_product_data(product.atvr_id)
            product.available_in_atvr = not not stock_info  # Forcing it to a boolean
            if verbose:
                if product.available_in_atvr:
                    availability = "available"
                else:
                    availability = "unavailable"
                print("Updating {}, {}".format(str(product), availability))
            product.atvr_stock = stock_info
            product.save()
            product.product_type.update_availability(verbose=verbose)
        renew_cache()
