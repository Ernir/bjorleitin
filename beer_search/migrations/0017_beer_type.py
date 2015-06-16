# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0016_beertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='type',
            field=models.ForeignKey(null=True, default=None, to='beer_search.BeerType'),
        ),
    ]
