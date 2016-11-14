import requests
from beer_search_v2.utils import renew_cache
from bs4 import BeautifulSoup
from beer_search_v2.models import Product
from django.core.exceptions import ObjectDoesNotExist
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

    def process_product(self, product, verbose=True):
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

    def add_arguments(self, parser):
        parser.add_argument(
                "--verbose",
                dest="verbose",
                help="specify how much the script should write",
                default=True,
                action="store_true"
        )
        parser.add_argument(
                "--item",
                dest="item",
                help="specify a particular product to update"
        )

    def handle(self, *args, **options):
        verbose = not not options["verbose"]
        if options["item"]:  # If an item is supplied, we only process that one
            try:
                product = Product.objects.get(atvr_id=options["item"])
                self.process_product(product, verbose)
            except ObjectDoesNotExist:
                print("Nothing found for {}.".format(options["item"]))
        else:  # Otherwise, we process them all
            products = Product.objects.filter(atvr_id__isnull=False).all()
            for product in products:
                self.process_product(product, verbose)
            renew_cache()
