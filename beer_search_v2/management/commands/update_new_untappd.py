from beer_search_v2.utils import update_untappd_item
from beer_search_v2.models import UntappdEntity
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        verbose = True
        entities = UntappdEntity.objects.filter(
            rating__isnull=True
        ).all()[0:100]
        for entity in entities:
            update_untappd_item(entity, verbose)
        if verbose:
            print("Entities updated")
