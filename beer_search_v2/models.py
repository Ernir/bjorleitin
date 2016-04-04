from django.db import models
from datetime import date, timedelta
from django.utils import timezone
from django.utils.text import slugify
from markdown import markdown


class ContainerType(models.Model):
    """

    Represents one type of beverage container: Can, bottle, etc.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Brewery(models.Model):
    name = models.CharField(max_length=500)
    alias = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        if self.alias is not None:
            return self.alias
        return self.name

    class Meta:
        verbose_name_plural = "breweries"
        ordering = ("name",)


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        first = self.name[0].upper()  # Enforce uppercase
        self.name = first + self.name[1:]
        super(Country, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "countries"
        ordering = ("name",)


class SimplifiedStyle(models.Model):
    """

    The styles as defined by the Untappd database are rather too numerous
    to allow for easy filtering. Each instance of UntappdStyle maps to one
    instance of this class, for easier filtering.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, default="", null=True)
    html_description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.html_description = markdown(self.description)
        super(SimplifiedStyle, self).save(*args, **kwargs)

    class Meta:
        ordering = ("name",)


class UntappdStyle(models.Model):
    """
    Represents one style, or "category" of beer (bjórstíll) as defined
    by the Untappd rating database.
    Examples include "Common Pale Lager" and "Dubbel".
    """

    name = models.CharField(max_length=100)
    simplifies_to = models.ForeignKey(SimplifiedStyle, null=True)

    def __str__(self):
        suffix = ""
        if self.simplifies_to:
            suffix = " ({0})".format(self.simplifies_to.name)
        return self.name + suffix

    class Meta:
        ordering = ("name",)


class UntappdEntity(models.Model):

    untappd_id = models.IntegerField(unique=True)
    brewery = models.ForeignKey(Brewery, null=True, default=None, blank=True)
    style = models.ForeignKey(UntappdStyle, null=True, default=None, blank=True)
    rating = models.FloatField(null=True, default=None, blank=True)


class ProductType(models.Model):
    """
    Denotes one 'type' of alcohol. A type can come in different containers. (A 330mL can of Tuborg Grøn is not the same
    product as a 500mL can, but it is the same ProductType).
    """

    # Base fields
    name = models.CharField(max_length=200, unique=True)
    abv = models.FloatField()

    # FK fields
    country = models.ForeignKey(Country, null=True, default=None, blank=True)
    untappd_info = models.ForeignKey(UntappdEntity)

    # Additional info
    available = models.BooleanField(default=False)
    needs_announcement = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def update_availability(self, verbose=True):
        any_available_product = False
        for product in self.product_set.all():
            if product.available:
                any_available_product = True
        # If there's a change, update
        if self.available != any_available_product:
            self.needs_announcement = True
            if verbose:
                if any_available_product:
                    print("{0} is now available".format(self.name))
                else:
                    print("{0} is no longer available".format(self.name))
            self.available = any_available_product
            self.save()

    class Meta:
        ordering = ("name",)


class Product(models.Model):
    """

    Represents one product, in one type of container at one particular volume.

    """

    # Core fields
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    volume = models.IntegerField()
    container = models.ForeignKey(ContainerType)
    product_id = models.CharField(max_length=100, unique=True)
    product_type = models.ForeignKey(ProductType)

    # Boolean/availability fields
    first_seen_at = models.DateTimeField(null=True)
    available = models.BooleanField(default=True)
    temporary = models.BooleanField(default=False)

    # Hidden fields
    updated_at = models.DateField(default=date.today)

    # Methods
    def __str__(self):
        name = "{0}, ({1} {2})".format(self.name, self.volume, self.container.name)
        return name

    def _price_per_litre(self):
        return int(self.price / self.volume * 1000)

    def _check_if_new(self):
        assert self.first_seen_at is not None

        two_months_ago = timezone.now() - timedelta(days=60)
        return self.first_seen_at > two_months_ago

    def save(self, *args, **kwargs):
        self.updated_at = date.today()  # Automatic updates
        super(Product, self).save(*args, **kwargs)

    # Properties
    price_per_litre = property(_price_per_litre)
    new = property(_check_if_new)

    class Meta:
        ordering = ("name", "container__name", "volume")
