# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-14 22:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0033_auto_20161114_2252'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductTypeList',
            new_name='ProductList',
        ),
    ]