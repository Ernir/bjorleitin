# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0042_auto_20160121_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beercategory',
            name='beers',
            field=models.ManyToManyField(blank=True, related_name='categories', to='beer_search.BeerType'),
        ),
        migrations.AlterField(
            model_name='beercategory',
            name='boxes',
            field=models.ManyToManyField(blank=True, related_name='categories', to='beer_search.GiftBox'),
        ),
    ]
