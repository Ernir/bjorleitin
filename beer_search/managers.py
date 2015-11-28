from django.db import models


class DefaultBeerManager(models.Manager):
    def get_common_related(self):
        return self.filter(available=True).select_related(
            "container",
            "beer_type",
            "beer_type__country",
            "beer_type__brewery",
            "beer_type__style",
            "beer_type__untappd_style__simplifies_to"
        )

    def available_beers(self):
        return self.filter(available=True)

    def get_queryset(self):
        return super(DefaultBeerManager, self). \
            get_queryset()


class DefaultGiftBoxManager(models.Manager):
    def get_common_related(self):
        return self.filter(available=True).select_related(
            "country"
        )