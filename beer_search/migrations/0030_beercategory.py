# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0029_auto_20151110_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeerCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.SlugField()),
                ('active', models.BooleanField()),
                ('beers', models.ManyToManyField(to='beer_search.BeerType')),
            ],
        ),
    ]
