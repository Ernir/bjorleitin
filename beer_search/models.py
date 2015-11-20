from beer_search.managers import DefaultBeerManager, DefaultGiftBoxManager
from django.db import models
from django.utils import timezone
from datetime import date, timedelta


class Style(models.Model):
    """

    Represents one style, or "category" of beer (bjórstíll).
    Examples include "Common Pale Lager" and "Dubbel".
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    def get_as_dict(self):
        """

        Returns a dictionary object representing this style.
        """
        return {
            "id": self.id,
            "name": self.name
        }

    class Meta:
        ordering = ("name",)


class ContainerType(models.Model):
    """

    Represents one type of beer container: Can, bottle, etc.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_as_dict(self):
        """

        Returns a dictionary object representing this container.
        """
        return {
            "id": self.id,
            "name": self.name
        }

    class Meta:
        ordering = ("name",)


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "countries"
        ordering = ("name",)


class Brewery(models.Model):
    name = models.CharField(max_length=500)
    untappd_id = models.IntegerField(unique=True)
    alias = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        if self.alias is not None:
            return self.alias
        return self.name

    class Meta:
        verbose_name_plural = "breweries"
        ordering = ("name",)


class BeerType(models.Model):
    """
    Denotes one 'type' of beer. A type of beer can come in different
    containers. (A 330mL can of Tuborg Grøn is not the same product (Beer)
    as a 500mL can, but it is the same BeerType.
    """

    # Base fields
    name = models.CharField(max_length=200, unique=True)
    abv = models.FloatField()

    # FK fields
    style = models.ForeignKey(Style, null=True, default=None)
    brewery = models.ForeignKey(Brewery, null=True, default=None, blank=True)
    country = models.ForeignKey(Country, null=True, default=None, blank=True)

    # Additional info
    untappd_id = models.IntegerField(null=True, default=None, blank=True)
    untappd_rating = models.FloatField(null=True, default=None, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name", )


class Beer(models.Model):
    """

    Represents one type of beer, in one type of container at one particular
    volume - A.K.A. one ATVR beer product.

    Objects of this type are heavyweight, forming the backbone of the app.
    """

    # Base fields
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    volume = models.IntegerField()
    atvr_id = models.CharField(max_length=5)

    # FK fields
    beer_type = models.ForeignKey(BeerType)
    container = models.ForeignKey(ContainerType)

    # Boolean/availability fields
    first_seen_at = models.DateTimeField(null=True)
    available = models.BooleanField(default=True)
    temporary = models.BooleanField(default=False)
    new = models.BooleanField(default=False)

    # Hidden fields
    updated_at = models.DateField(default=date.today)
    suffix = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name + self.suffix

    def calculate_uniquely_identifying_suffix(self):
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
        n = Beer.objects.filter(name=self.name, available=True).count()
        return n > 1

    def _has_duplicate_container(self):
        n = Beer.objects.filter(name=self.name, container=self.container) \
            .count()
        return n > 1

    def _price_per_litre(self):
        return int(self.price / self.volume * 1000)

    def _check_if_new(self):
        if not self.first_seen_at:
            return False  # If we've never seen it, it's not a new product.
        two_months_ago = timezone.now() - timedelta(days=60)

        return self.first_seen_at > two_months_ago

    has_duplicate_name = property(_has_duplicate_name)
    has_duplicate_container = property(_has_duplicate_container)
    price_per_litre = property(_price_per_litre)

    objects = DefaultBeerManager()

    def update_duplicates(self):
        new_suffix = self.calculate_uniquely_identifying_suffix()
        if new_suffix != self.suffix:
            self.suffix = new_suffix
            print("Updating duplicates for {0}".format(self.name))
            self.save()
        duplicates = Beer.objects \
            .filter(name=self.name, beer_type__style=None) \
            .exclude(atvr_id=self.atvr_id)
        for duplicate in duplicates:
            new_suffix = duplicate.calculate_uniquely_identifying_suffix()
            if new_suffix != duplicate.suffix:
                self.suffix = new_suffix
                duplicate.save()

    def save(self, *args, **kwargs):
        self.updated_at = date.today()  # Automatic updates
        self.new = self._check_if_new()

        super(Beer, self).save(*args, **kwargs)

    def get_as_dict(self):
        """

        Returns a human-readable dictionary object representing the beer.
        """

        return {
            "name": self.name,
            "style": self.beer_type.style.name,
            "container": self.container.name,
            "abv": self.beer_type.abv,
            "volume": self.volume,
            "price": self.price,
            "atvr_id": self.atvr_id
        }

    class Meta:
        ordering = ("name", "container__name")


class GiftBox(models.Model):
    """

    Represents one type of gift box. Giftboxes are similar to beers (see
    above), but do not have a beer type (usually there are multiple types
    per box) and similar.

    """

    # Base fields
    name = models.CharField(max_length=200)
    abv = models.FloatField()
    price = models.IntegerField()
    volume = models.IntegerField()
    atvr_id = models.CharField(max_length=5)

    # FK fields
    country = models.ForeignKey(Country, null=True, default=None)

    # Boolean/availability fields
    first_seen_at = models.DateTimeField(null=True)
    available = models.BooleanField(default=True)
    temporary = models.BooleanField(default=False)
    new = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def _check_if_new(self):
        if not self.first_seen_at:
            return False  # If we've never seen it, it's not a new product.
        two_months_ago = timezone.now() - timedelta(days=60)

        return self.first_seen_at > two_months_ago

    objects = DefaultGiftBoxManager()

    def save(self, *args, **kwargs):
        self.new = self._check_if_new()

        super(GiftBox, self).save(*args, **kwargs)

    def get_as_dict(self):
        """

        Returns a human-readable dictionary object representing the box.
        """

        return {
            "name": self.name,
            "abv": self.abv,
            "volume": self.volume,
            "price": self.price,
            "atvr_id": self.atvr_id
        }

    class Meta:
        verbose_name_plural = "gift boxes"
        ordering = ("name",)


class Region(models.Model):
    """
    Represents one region of Iceland.
    Used to categorize the stores.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Store(models.Model):
    """
    Represents a store.
    """

    # Usually just the location
    location = models.CharField(max_length=200)
    region = models.ForeignKey(Region)

    # The name used in the scraped data itself.
    reference_name = models.CharField(max_length=100)
    beers_available = models.ManyToManyField(Beer)

    def __str__(self):
        return self.region.name + ": " + self.location

    class Meta:
        ordering = ("region__name", "location")


class BeerCategory(models.Model):
    """
    A simple class to arbitrarily categorize beers (BeerTypes).
    """
    name = models.CharField(max_length=200)
    url = models.SlugField()
    active = models.BooleanField()
    description = models.TextField(blank=True, default="")
    beers = models.ManyToManyField(BeerType, related_name="categories")
    boxes = models.ManyToManyField(GiftBox, related_name="categories")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "beer categories"


class ModifiableSettings(models.Model):
    """
    Each instance represents one "setting" modifiable in the admin.
    """

    key = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return self.key + ": " + str(self.value)

    class Meta:
        verbose_name_plural = "modifiable settings"