from beer_search_v2.utils import renew_cache
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        renew_cache()
