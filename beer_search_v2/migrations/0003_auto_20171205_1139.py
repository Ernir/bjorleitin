# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-05 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0002_auto_20171205_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atvrproduct',
            name='atvr_id',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]