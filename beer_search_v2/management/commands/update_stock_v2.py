import requests
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
            print("Could not establish a connection to ATVR.")
            # Defaults to an undefined stock
            return None

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
        products = Product.objects.filter(available_in_atvr=True).all()
        for product in products:
            if verbose:
                print("Updating {}".format(str(product)))
            stock_info = self.get_product_data(product.atvr_id)
            product.atvr_stock = stock_info
            product.save()
