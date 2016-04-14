import csv
import re
from beer_search_v2.models import Product, ContainerType, ProductType
from beer_search_v2.utils import get_alcohol_category_instance
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from datetime import date


class Command(BaseCommand):
    @classmethod
    def prepare_products_for_update(cls):
        # Marking all existing products from Járn og Gler as not available until proven wrong.
        for product in Product.objects.filter(source=Product.JoG).all():
            product.available = False
            product.save()

    @classmethod
    def update_products(cls, product_list):

        for data_row in product_list:
            product = cls.get_product_instance(data_row)
            cls.update_product_type(product, data_row)
            product.available = True
            new_price = cls.extract_price(data_row[4])
            product.price = new_price  # We always update the price

            product.save()

    @classmethod
    def get_product_instance(cls, data_row):
        product_id = data_row[0]
        try:  # Checking if we've found the product previously
            product = Product.objects.get(jog_id=product_id)
        except ObjectDoesNotExist:
            product = Product()
            product.jog_id = product_id
            cls.initialize_product(product, data_row)
        return product

    @classmethod
    def initialize_product(cls, product, data_row):
        raw_product_name = data_row[1]  # This is usually a terrible name, but it's what we have
        print("Creating new product: " + raw_product_name)
        product.name = raw_product_name
        product.price = cls.extract_price(data_row[4])
        product.volume = cls.guess_volume(raw_product_name)
        product.first_seen_at = date.today()
        product.container = cls.guess_container_type(product.name)
        product.source = Product.JoG
        return product

    @classmethod
    def update_product_type(cls, product, data_row):
        """
        Each product is an instance of a particular product type, this common info is stored separately.
        """
        try:  # Checking if this product belongs to type with the same name
            product_type = ProductType.objects.get(name=product.name)
            product.product_type = product_type
        except ObjectDoesNotExist:  # Otherwise, create one
            product_type = ProductType()
            product_type.name = product.name
            product_type.abv = cls.guess_abv(product.name)
            product_type.country = None
            product_type.alcohol_category = get_alcohol_category_instance("beer")
            product_type.save()

            product.product_type = product_type

            print("Creating new product type: {0}".format(product_type.name))
        product.save()

    @classmethod
    def guess_container_type(cls, raw_name):
        if "dós" in raw_name:
            return ContainerType.objects.get(name="Dós")
        else:
            return ContainerType.objects.get(name="Flaska")

    @classmethod
    def guess_volume(cls, raw_name):
        m = re.search("(?P<volume>\d+)( ?)ml", raw_name)
        if m:
            return int(m.group("volume"))
        elif "1/3" in raw_name:
            return 330
        print("Warning, no volume found for {0}".format(raw_name))
        return 0

    @classmethod
    def guess_abv(cls, raw_name):
        m = re.search("(?P<abv>\d+|\d+,\d+)%", raw_name)
        if m:
            return float(m.group("abv").replace(",","."))
        print("Warning, no abv found for {0}".format(raw_name))
        return 0

    @classmethod
    def extract_price(cls, price_string):
        # Price strings are dirty and require extraction
        return int("".join([c for c in price_string if c.isdigit()]))

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        product_list = []
        with open(options["filename"], newline='') as csvfile:
            product_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in product_reader:
                if row[0]:  # Some rows have no contents
                    product_list.append(row)

        if len(product_list) > 0:
            self.prepare_products_for_update()
            self.update_products(product_list)

        for product_type in ProductType.objects.filter().all():
            product_type.update_availability(verbose=False)
