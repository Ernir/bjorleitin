# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-14 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0031_producttypelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttypelist',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]