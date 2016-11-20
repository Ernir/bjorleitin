from beer_search_v2.models import ProductType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Displays those product types which would be announced on running the announce management task
        """
        product_types = ProductType.objects.filter(needs_announcement=True).all()
        if product_types:
            print("These product types will be announced: ")
            print("\n".join([p.alias for p in product_types]))
        else:
            print("No product types are in need of announcement.")
