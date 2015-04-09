from django.db import models
from datetime import date


class Style(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class ContainerType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
            return self.name

    class Meta:
        ordering = ("name",)


class Beer(models.Model):

    name = models.CharField(max_length=200)
    abv = models.FloatField()
    price = models.IntegerField()
    volume = models.IntegerField()
    atvr_id = models.CharField(max_length=5)

    container = models.ForeignKey(ContainerType, null=True, default=None)
    style = models.ManyToManyField(Style)

    updated_at = models.DateField(default=date.today)

    def __str__(self):
        if self.container:
            return self.name + " ( " + str(self.volume) + "mL " + self.container.name + " )"
        else:
            return self.name + " ( " + str(self.volume) + "mL )"

    def save(self, *args, **kwargs):
        self.updated_at = date.today()  # Automatic updates
        super(Beer, self).save(*args, **kwargs)

    class Meta:
        ordering = ("name",)