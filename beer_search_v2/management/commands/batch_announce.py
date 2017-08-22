from beer_search_v2.models import ProductType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Prints out a markdown-formatted list of products that can be posted as a whole
        """
        product_types = ProductType.objects.filter(needs_announcement=True)
        if product_types:
            for p in product_types.all():
                print("[{}](http://bjorleit.info{})\n".format(p.alias, p.get_absolute_url()))
                p.needs_announcement = False
                p.save()
            print("{} vörur alls".format(product_types.count()))
        else:
            print("No product types are in need of announcement.")
