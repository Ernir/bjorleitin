# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0003_auto_20160406_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='source',
            field=models.IntegerField(default=0, choices=[(0, 'ÁTVR'), (1, 'Járn og Gler')]),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='alcohol_category',
            field=models.ForeignKey(to='beer_search_v2.AlcoholCategory'),
        ),
    ]
