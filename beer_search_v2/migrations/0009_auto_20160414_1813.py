# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0008_auto_20160414_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='jog_id',
            field=models.CharField(unique=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='atvr_id',
            field=models.CharField(unique=True, max_length=100, null=True),
        ),
    ]
