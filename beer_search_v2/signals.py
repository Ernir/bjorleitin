from django.db import IntegrityError
from random import sample

from beer_search_v2.models import Country, Brewery, SimplifiedStyle, ProductType, Product
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from markdown import markdown
from datetime import date


@receiver(pre_save, sender=Country)
def capitalize_country_name(sender, instance, **kwargs):
    instance.name = instance.name[0].upper() + instance.name[:1]


@receiver(pre_save, sender=Brewery)
def initialize_brewery_alias(sender, instance, **kwargs):
    if not instance.alias:
        instance.alias = instance.name


@receiver(pre_save, sender=SimplifiedStyle)
def update_simplifiedstyle_examples(sender, instance, **kwargs):
    # Finding all product types associated with a particular simplified style
    product_types = set()
    untappd_styles = instance.untappdstyle_set.all()
    for untappd_style in untappd_styles:
        for entity in untappd_style.untappdentity_set.all():
            for product_type in entity.producttype_set.filter(available=True).all():
                product_types.add(product_type)

    # Randomly picking five of those product types
    sample_size = min(5, len(product_types))
    examples = sample(product_types, sample_size)

    instance.examples.clear()
    for example in examples:
        instance.examples.add(example)

    instance.slug = slugify(instance.name)
    instance.html_description = markdown(instance.description)


@receiver(pre_save, sender=ProductType)
def initialize_producttype_alias(sender, instance, **kwargs):
    if not instance.alias:
        instance.alias = instance.name


@receiver(pre_save, sender=ProductType)
def initialize_producttype_image(sender, instance, **kwargs):
    if not instance.main_image:
        instance.update_image_url()


@receiver(pre_save, sender=Product)
def clean_product(sender, instance, **kwargs):
    instance.name = instance.name.strip()  # For everyone's sanity
    instance.updated_at = date.today()  # Automatic updates
    if not instance.image_url:
        instance.attempt_image_fetch()


@receiver(post_save, sender=Product)
def validate_product(sender, instance, created, **kwargs):
    # ToDo: Test this logic
    max_duplicates_allowed = 1 # Products should not share non-falsey identifiers
    if instance.atvr_id:
        if Product.objects.filter(atvr_id=instance.atvr_id).count() > max_duplicates_allowed:
            raise IntegrityError("Product with given ÁTVR ID already exists")
    if instance.jog_id:
        if Product.objects.filter(jog_id=instance.jog_id).count() > max_duplicates_allowed:
            raise IntegrityError("Product with given Járn og Gler ID already exists")
