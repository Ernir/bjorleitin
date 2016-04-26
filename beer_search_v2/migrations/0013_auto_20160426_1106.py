# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0012_auto_20160420_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brewery',
            name='country_name',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
    ]
