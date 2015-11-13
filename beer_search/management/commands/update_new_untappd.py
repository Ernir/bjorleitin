from beer_search.utils import update_untappd_item
from beer_search.models import BeerType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        beer_types = BeerType.objects.filter(
            untappd_id__isnull=False,
            untappd_rating__isnull=True
        ).all()
        for beer_type in beer_types:
            update_untappd_item(beer_type)