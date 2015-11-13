# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0031_auto_20151112_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beercategory',
            name='beers',
            field=models.ManyToManyField(to='beer_search.BeerType', related_name='categories'),
        ),
        migrations.AlterField(
            model_name='beercategory',
            name='boxes',
            field=models.ManyToManyField(to='beer_search.GiftBox', related_name='categories'),
        ),
    ]
