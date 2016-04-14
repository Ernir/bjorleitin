# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0005_auto_20160407_2311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alcoholcategory',
            options={'verbose_name_plural': 'Alcohol categories'},
        ),
        migrations.AlterModelOptions(
            name='untappdentity',
            options={'ordering': ('untappd_id',), 'verbose_name_plural': 'Untappd entities'},
        ),
    ]
