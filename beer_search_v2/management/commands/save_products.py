from beer_search_v2.models import Product
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Performs the save() operation on each of the Product objects
        """
        products = Product.objects
        if products:
            for p in products.all():
                p.save()
            print("Saved {} products".format(products.count()))
        else:
            print("There are no products to save.")
