# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0028_auto_20151110_1639'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brewery',
            options={'verbose_name_plural': 'breweries', 'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='giftbox',
            options={'verbose_name_plural': 'gift boxes', 'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='modifiablesettings',
            options={'verbose_name_plural': 'modifiable settings'},
        ),
    ]
