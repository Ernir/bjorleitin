# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0009_auto_20160414_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='atvr_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='jog_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
