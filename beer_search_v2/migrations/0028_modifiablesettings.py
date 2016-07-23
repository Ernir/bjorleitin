# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-21 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0027_product_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModifiableSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'modifiable settings',
            },
        ),
    ]
