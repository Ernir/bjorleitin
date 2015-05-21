# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0014_auto_20150521_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='beers_available',
            field=models.ManyToManyField(to='beer_search.Beer'),
        ),
    ]
