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
    style = models.ForeignKey(Style, null=True, default=None)

    updated_at = models.DateField(default=date.today)

    def __str__(self):
        name = self.name
        if self.has_duplicate_name:
            if not self.container:
                name += " ( ?"
            else:
                name = name + " ( " + self.container.name
            if self.has_duplicate_container:
                name = name + ", " + str(self.volume) + " mL"
            name += " )"
        return name

    def _has_duplicate_name(self):
        n = Beer.objects.filter(name=self.name).count()
        return n > 1

    def _has_duplicate_container(self):
        n = Beer.objects.filter(name=self.name, container=self.container).count()
        return n > 1

    def _price_per_litre(self):
        return int(self.price / self.volume * 1000)

    has_duplicate_name = property(_has_duplicate_name)
    has_duplicate_container = property(_has_duplicate_container)
    price_per_litre = property(_price_per_litre)

    def save(self, *args, **kwargs):
        self.updated_at = date.today()  # Automatic updates

        # Finds beers with the same name, and assigns the same style.
        if self.style:
            duplicates = Beer.objects\
                .filter(name=self.name, style=None)\
                .exclude(atvr_id=self.atvr_id)
            if duplicates.count() > 0:
                # Sometimes superfluous saving, but meh.
                super(Beer, self).save(*args, **kwargs)
            for beer in duplicates.all():
                beer.style = self.style
                beer.save()

        super(Beer, self).save(*args, **kwargs)

    class Meta:
        ordering = ("name","container__name")