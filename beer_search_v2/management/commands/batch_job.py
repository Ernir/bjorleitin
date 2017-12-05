from django.core.exceptions import ObjectDoesNotExist

from beer_search_v2.models import Product, ATVRProduct, UntappdEntity, JoGProduct
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        This is a dumb script to perform one-off-maintenance.
        """

        # Copy over old-style Product data
        products = []  # Product.objects.filter(atvr_id__isnull=False).all():
        for p in products:
            try:
                newp = ATVRProduct.objects.get(atvr_id=p.atvr_id)
                created = False
            except ObjectDoesNotExist:
                newp = ATVRProduct()
                newp.atvr_id = p.atvr_id
                created = True
            newp.name = p.name
            newp.price = p.price
            newp.volume = p.volume
            newp.container = self.get_container(p.container.name)
            if p.product_type.untappd_info_id:
                newp.untappd_info = p.product_type.untappd_info
            newp.first_seen_at = p.first_seen_at
            newp.temporary = p.temporary
            newp.atvr_stock = p.atvr_stock
            newp.updated_at = p.updated_at
            newp.image_url = p.updated_at

            newp.save()
            if created:
                print("Created {}".format(newp))
            else:
                print("Updated {}".format(newp))

        for p in Product.objects.filter(jog_id__isnull=False).all():
            try:
                newp = JoGProduct.objects.get(jog_id=p.jog_id)
                created = False
            except ObjectDoesNotExist:
                newp = JoGProduct()
                newp.jog_id = p.jog_id
                created = True
            newp.name = p.name
            newp.price = p.price
            newp.volume = p.volume
            newp.container = self.get_container(p.container.name)
            if p.product_type.untappd_info_id:
                newp.untappd_info = p.product_type.untappd_info
            newp.first_seen_at = p.first_seen_at
            newp.available_in_jog = p.available_in_jog
            newp.updated_at = p.updated_at

            newp.save()
            if created:
                print("Created {}".format(newp))
            else:
                print("Updated {}".format(newp))

    def get_container(self, container_long_name):
        CONTAINER_CHOICES = (
            ("DS.", "Dós"),
            ("FL.", "Flaska"),
            ("KÚT", "Kútur"),
            ("ASKJA", "Gjafaaskja"),
            ("ANNAD", "Ótilgreint")
        )

        for short, long in CONTAINER_CHOICES:
            if container_long_name == long:
                return short
        return "ANNAD"
