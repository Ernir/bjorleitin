from django.db import models
from datetime import date


class Style(models.Model):
    """

    Represents one style, or "category" of beer (bjórstíll).
    Examples include "Common Pale Lager" and "Dubbel".
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class ContainerType(models.Model):
    """

    Represents one type of beer container: Can, bottle, etc.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Beer(models.Model):
    """

    Represents one type of beer, in one type of container at one particular
    volume - A.K.A. one ATVR product.

    Objects of this type are heavyweight, forming the backbone of the app.
    """

    # Base fields
    name = models.CharField(max_length=200)
    abv = models.FloatField()
    price = models.IntegerField()
    volume = models.IntegerField()
    atvr_id = models.CharField(max_length=5)

    # FK fields
    container = models.ForeignKey(ContainerType, null=True, default=None)
    style = models.ForeignKey(Style, null=True, default=None)

    # Boolean/availability fields
    new = models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    seasonal = models.BooleanField(default=False)

    # Hidden fields
    updated_at = models.DateField(default=date.today)
    suffix = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name + self.suffix

    def _calculate_uniquely_identifying_suffix(self):
        """

        Many beers have non-unique names, due to different volumes and
        container types counting as separate ATVR products.
        If [self.name] is not unique among beer objects, this generates
        and returns a human-readable, uniquely-identifying string.
        Otherwise, returns empty string.
        """
        suffix = ""
        if self.has_duplicate_name:
            if not self.container:
                suffix += " ( ?"  # Unknown container placeholder
            else:
                suffix = suffix + " ( " + self.container.name
            if self.has_duplicate_container:
                suffix = suffix + ", " + str(self.volume) + " mL"
            suffix += " )"
        return suffix

    def _has_duplicate_name(self):
        n = Beer.objects.filter(name=self.name).count()
        return n > 1

    def _has_duplicate_container(self):
        n = Beer.objects.filter(name=self.name, container=self.container) \
            .count()
        return n > 1

    def _price_per_litre(self):
        return int(self.price / self.volume * 1000)

    has_duplicate_name = property(_has_duplicate_name)
    has_duplicate_container = property(_has_duplicate_container)
    price_per_litre = property(_price_per_litre)

    def save(self, *args, **kwargs):
        self.updated_at = date.today()  # Automatic updates

        self.suffix = self._calculate_uniquely_identifying_suffix()
        # Finds beers with the same name, and assigns the same style.
        if self.style:
            duplicates = Beer.objects \
                .filter(name=self.name, style=None) \
                .exclude(atvr_id=self.atvr_id)
            if duplicates.count() > 0:
                # Sometimes superfluous saving, but meh.
                super(Beer, self).save(*args, **kwargs)
            for beer in duplicates.all():
                beer.style = self.style
                beer.save()

        super(Beer, self).save(*args, **kwargs)

    class Meta:
        ordering = ("name", "container__name")