# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0025_giftbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beer',
            name='abv',
        ),
        migrations.AlterField(
            model_name='beer',
            name='beer_type',
            field=models.ForeignKey(to='beer_search.BeerType'),
        ),
        migrations.AlterField(
            model_name='beer',
            name='container',
            field=models.ForeignKey(to='beer_search.ContainerType'),
        ),
    ]
