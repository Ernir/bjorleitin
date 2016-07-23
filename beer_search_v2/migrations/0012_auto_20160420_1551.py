# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0011_brewery_untappd_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewery',
            name='country',
            field=models.ForeignKey(to='beer_search_v2.Country', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='brewery',
            name='country_name',
            field=models.CharField(default='Norway', max_length=200),
            preserve_default=False,
        ),
    ]
