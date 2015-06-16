# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0015_store_beers_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('abv', models.FloatField()),
                ('untappd_id', models.IntegerField(blank=True, default=None, null=True)),
                ('untappd_rating', models.FloatField(blank=True, default=None, null=True)),
                ('country', models.ForeignKey(to='beer_search.Country', default=None, null=True)),
                ('style', models.ForeignKey(to='beer_search.Style', default=None, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
