# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-01 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0036_auto_20161120_1629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productlist',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='untappdentity',
            options={'ordering': ('untappd_name',), 'verbose_name_plural': 'Untappd entities'},
        ),
        migrations.RemoveField(
            model_name='untappdentity',
            name='product_name',
        ),
        migrations.AddField(
            model_name='untappdentity',
            name='logo_url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='untappdentity',
            name='untappd_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
