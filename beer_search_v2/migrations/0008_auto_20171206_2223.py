# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-06 22:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0007_auto_20171206_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='untappdentity',
            name='abv',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='untappdentity',
            name='ibu',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
