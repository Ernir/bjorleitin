# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0032_auto_20151113_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beertype',
            name='brewery',
            field=models.ForeignKey(null=True, to='beer_search.Brewery', blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='beertype',
            name='country',
            field=models.ForeignKey(null=True, to='beer_search.Country', blank=True, default=None),
        ),
    ]
