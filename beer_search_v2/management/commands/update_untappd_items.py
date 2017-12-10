from beer_search_v2.utils import update_untappd_item
from beer_search_v2.models import ModifiableSetting, UntappdEntity
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        self.verbose = True
        super().__init__()

    def get_indices(self):
        """

        The untappd API is rate limited, the list needs to be limited as well.
        """
        mod_settings = ModifiableSetting.objects

        start_index_setting = mod_settings.get(key="untappd_start_index")
        num_per_run_setting = mod_settings.get(key="untappd_items_per_run")

        start_index = start_index_setting.value
        end_index = start_index_setting.value + num_per_run_setting.value

        return start_index, end_index

    def update_indices(self, end_index):
        start_index_setting = ModifiableSetting.objects.get(key="untappd_start_index")

        num_items = UntappdEntity.objects.count()

        if end_index > num_items:  # We've finished the list for now, resetting
            start_index_setting.value = 0
        else:  # Next time, we start further into the list.
            start_index_setting.value = end_index

        start_index_setting.save()

    def add_arguments(self, parser):
        parser.add_argument(
                "--verbose",
                dest="verbose",
                help="specify how much the script should write",
                default=True,
                action="store_true"
        )

    def handle(self, *args, **options):
        self.verbose = not not options["verbose"]
        untappd_entities = UntappdEntity.objects.all()
        start_index, end_index = self.get_indices()
        for entity in untappd_entities[start_index:end_index]:
            update_untappd_item(entity, self.verbose)
        self.update_indices(end_index)
