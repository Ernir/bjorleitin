from beer_search_v2.utils import get_main_display
from beer_search_v2.models import MainQueryResult
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = get_main_display()
        MainQueryResult.objects.create(json_contents=data)
