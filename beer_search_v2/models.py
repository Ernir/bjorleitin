import requests
from random import sample

from django.contrib.postgres.fields import JSONField
from django.db import models, IntegrityError
from django.core.urlresolvers import reverse
from datetime import date, timedelta
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
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


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            first = self.name[0].upper()  # Enforce uppercase
            self.name = first + self.name[1:]
        else:
            raise ValueError("Attempted to save a Country instance without providing a name")
        super(Country, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "countries"
        ordering = ("name",)


class Brewery(models.Model):
    name = models.CharField(max_length=500)
    untappd_id = models.IntegerField(unique=True)
    alias = models.CharField(max_length=500, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    country_name = models.CharField(max_length=200, null=True, blank=True)  # Redundancy, used as a fallback

    def __str__(self):
        if self.alias:
            return self.alias
        return self.name

    class Meta:
        verbose_name_plural = "breweries"
        ordering = ("name",)


class SimplifiedStyle(models.Model):
    """

    The styles as defined by the Untappd database are rather too numerous
    to allow for easy filtering. Each instance of UntappdStyle maps to one
    instance of this class, for easier filtering.
    """

    name = models.CharField(max_length=100)
    name_in_sentence = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, default="", null=True)
    html_description = models.TextField()
    examples = models.ManyToManyField("ProductType", blank=True)  # String specification due to circular reference

    def get_absolute_url(self):
        return "{}#{}".format(reverse("styles"), self.slug)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        product_types = set()
        untappd_styles = self.untappdstyle_set.all()
        for untappd_style in untappd_styles:
            for entity in untappd_style.untappdentity_set.all():
                for product_type in entity.producttype_set.all():
                    product_types.add(product_type)

        sample_size = min(5, len(product_types))
        examples = sample(product_types, sample_size)

        self.examples.clear()
        for example in examples:
            self.examples.add(example)

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
    """
    Maintains information coming from the Untappd rating database.
    """
    untappd_id = models.IntegerField(unique=True)
    brewery = models.ForeignKey(Brewery, null=True, default=None, blank=True)
    style = models.ForeignKey(UntappdStyle, null=True, default=None, blank=True)
    rating = models.FloatField(null=True, default=None, blank=True)

    product_name = models.CharField(max_length=200, default="UNKNOWN")

    def save(self, *args, **kwargs):
        if self.producttype_set.count() > 0:
            self.product_name = str(self.producttype_set.first())
        super(UntappdEntity, self).save(*args, **kwargs)

    def __str__(self):
        return str("{0} ({1})".format(self.product_name, self.untappd_id))

    class Meta:
        ordering = ("untappd_id",)
        verbose_name_plural = "Untappd entities"


class AlcoholCategory(models.Model):
    """
    Denotes one category of alcohols, e.g. "red wine".
    """
    name = models.CharField(max_length=200, unique=True)
    alias = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.alias:
            return self.alias
        return self.name

    class Meta:
        verbose_name_plural = "Alcohol categories"


class ProductType(models.Model):
    """
    Denotes one 'type' of product. A type of the same alcohol can come in different containers.
    (A 330mL can of Tuborg Grøn is not the same product as a 500mL can, but it is the same ProductType).
    """

    # Base fields
    name = models.CharField(max_length=200, unique=True)
    alias = models.CharField(max_length=200, blank=True)
    abv = models.FloatField()

    # FK fields
    country = models.ForeignKey(Country, null=True, default=None, blank=True)
    untappd_info = models.ForeignKey(UntappdEntity, null=True, default=None, blank=True)
    alcohol_category = models.ForeignKey(AlcoholCategory)

    # Additional info
    available = models.BooleanField(default=False)
    needs_announcement = models.BooleanField(default=False)

    # Fluff
    main_image = models.URLField(default="", blank=True)

    # Methods

    def _update_image_url(self):
        for product in self.product_set.all():
            if product.image_url:
                self.main_image = product.image_url
                self.save()
                return

    def _is_relevant(self):
        if self.product_set.count() == 1 and self.product_set.all()[0].container.name in ["Gjafaaskja", "Kútur"]:
            return False
        return not not self.untappd_info or self.alcohol_category.name == "beer"

    def save(self, *args, **kwargs):
        if not self.alias:  # Aliases are used for sorting
            self.alias = self.name
        super(ProductType, self).save(*args, **kwargs)

    def __str__(self):
        if self.alias:
            return self.alias
        return self.name

    def get_absolute_url(self):
        return reverse("single_product", kwargs={"pid": self.id})

    def update_availability(self, verbose=True):
        any_available_product = False
        for product in self.product_set.all():
            if product.available_in_atvr or product.available_in_jog:
                any_available_product = True
        # If there's a change, update
        if self.available != any_available_product and self.is_relevant:
            self.needs_announcement = True
            if verbose:
                if any_available_product:
                    print("{0} is now available".format(self.name))
                else:
                    print("{0} is no longer available".format(self.name))
            self.available = any_available_product
            self.save()

    class Meta:
        ordering = ("alias",)

    # Properties

    is_relevant = property(_is_relevant)


class Product(models.Model):
    """

    Represents one product, in one type of container at one particular volume.

    """

    # Core fields
    name = models.CharField(max_length=200)
    price = models.IntegerField(null=True)
    volume = models.IntegerField(null=True)
    container = models.ForeignKey(ContainerType)
    product_type = models.ForeignKey(ProductType)

    # The two current product sources use different identification systems
    atvr_id = models.CharField(max_length=100, null=True, blank=True)
    jog_id = models.CharField(max_length=100, null=True, blank=True)

    # Boolean/availability fields
    first_seen_at = models.DateTimeField(null=True)
    available_in_atvr = models.BooleanField(default=False)
    available_in_jog = models.BooleanField(default=False)
    temporary = models.BooleanField(default=False)
    atvr_stock = JSONField(default={}, blank=True)

    # Read-only fields
    updated_at = models.DateField(default=date.today)

    # Fluff
    image_url = models.URLField(default="", blank=True)

    # Methods
    def __str__(self):
        name = "{0}, ({1}ml {2})".format(self.name, self.volume, self.container.name)
        return name

    def _price_per_litre(self):
        return int(self.price / self.volume * 1000)

    def _check_if_new(self):
        assert self.first_seen_at is not None

        two_months_ago = timezone.now() - timedelta(days=60)
        return self.first_seen_at > two_months_ago

    def _attempt_image_fetch(self):
        if self.atvr_id and not self.image_url:
            url = "http://www.vinbudin.is/Portaldata/1/Resources/vorumyndir/original/{}_r.jpg".format(self.atvr_id)
            r = requests.get(url)
            if r.status_code == 200:
                self.image_url = url
                self.save()

    def get_absolute_url(self):
        return self.product_type.get_absolute_url()

    def save(self, *args, **kwargs):
        self.name = self.name.strip()  # For everyone's sanity
        self.updated_at = date.today()  # Automatic updates

        # Products should not share non-falsey identifiers
        # ToDo validate creation and saving differently. Currently assumes saving
        if self.atvr_id:
            if Product.objects.filter(atvr_id=self.atvr_id).count() > 1:
                raise IntegrityError("Product with given ÁTVR ID already exists")
        if self.jog_id:
            if Product.objects.filter(jog_id=self.jog_id).count() > 1:
                raise IntegrityError("Product with given Járn og Gler ID already exists")

        super(Product, self).save(*args, **kwargs)

    # Properties
    price_per_litre = property(_price_per_litre)
    new = property(_check_if_new)

    class Meta:
        ordering = ("name", "container__name", "volume")


class MainQueryResult(models.Model):
    """
    Does not represent an actual entity.
    Used for queryset caching, storing results in JSON format.
    """

    json_contents = JSONField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ("-created_at",)


class ModifiableSetting(models.Model):
    """
    Each instance represents one "setting" modifiable in the admin.
    """

    key = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return self.key + ": " + str(self.value)

    class Meta:
        verbose_name_plural = "modifiable settings"
