# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0006_auto_20160414_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='untappdentity',
            name='product_name',
            field=models.CharField(max_length=200, default='UNKNOWN'),
        ),
    ]
