# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0023_auto_20150803_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='beer_type',
            field=models.ForeignKey(null=True, default=None, blank=True, to='beer_search.BeerType'),
        ),
    ]
