# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-07 18:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0017_producttype_alternate_names'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='available',
            new_name='available_in_atvr',
        ),
    ]