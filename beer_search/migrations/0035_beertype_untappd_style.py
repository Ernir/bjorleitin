# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0034_untappdstyle'),
    ]

    operations = [
        migrations.AddField(
            model_name='beertype',
            name='untappd_style',
            field=models.ForeignKey(null=True, blank=True, to='beer_search.UntappdStyle', default=None),
        ),
    ]
