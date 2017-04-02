import requests
from bs4 import BeautifulSoup
from beer_search_v2.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        self.verbose = True
        super().__init__()

    def get_product_data(self, atvr_id):
        """
        :param atvr_id: The ID of one of ATVR's products.
        :return: A dictionary consisting of store names as keys, and the
        stock status of the product with the given ID as values.
        """

        base_url = "http://www.vinbudin.is/Heim/v%C3%B6rur/stoek-vara.aspx/"
        params = {"productID": atvr_id}

        # Defaults to an empty stock and no price change
        product_info = {"success": False, "stores": [], "price": None}
        try:
            html_doc = requests.get(base_url, params=params).text
        except ConnectionError:
            print("Could not establish a connection to ATVR for product {}".format(atvr_id))
            return product_info

        soup = BeautifulSoup(html_doc, 'html.parser')

        # First we try to find stock statuses for various
        stock_status = soup.find(id="div-stock-status")
        if stock_status:
            store_names = stock_status.find_all(class_="store")
        else:
            store_names = []  # If the div can't be found, conclude the stock is empty.
        store_info = []
        for store in store_names:
            store_info.append({"store": store.string, "stock": int(store.next_sibling.string)})
        product_info["stores"] = store_info

        # Then we find the product's current price
        price = soup.find(class_="money")
        if price:
            product_info["price"] = int("".join([c for c in price.string if c.isdigit()]))

        product_info["success"] = True
        return product_info

    def process_product(self, product):
        data = self.get_product_data(product.atvr_id)
        product.available_in_atvr = not not data["stores"] and data["success"]  # Forcing it to a boolean
        if not not data["price"] and data["success"]:
            new_price = data["price"]
            if new_price != product.price and self.verbose:
                print("Price change for {}, changing from {} to {} krónur".format(
                        str(product), product.price, new_price)
                )
            product.price = new_price
        if self.verbose:
            if product.available_in_atvr:
                availability = "available"
            else:
                availability = "unavailable"
            print("Updating {}, {}".format(str(product), availability))

        product.atvr_stock = data["stores"]
        product.save()
        product.product_type.update_availability(verbose=self.verbose)

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
        self.verbose = not not options["verbose"]
        if options["item"]:  # If an item is supplied, we only process that one
            try:
                product = Product.objects.get(atvr_id=options["item"])
                self.process_product(product)
            except ObjectDoesNotExist:
                print("Nothing found for {}.".format(options["item"]))
        else:  # Otherwise, we process them all
            products = Product.objects.filter(atvr_id__isnull=False).all()
            for product in products:
                self.process_product(product)
