from django.db import models


class AvailableBeersManager(models.Manager):
    def get_queryset(self):
        return super(AvailableBeersManager, self). \
            get_queryset().filter(available=True)