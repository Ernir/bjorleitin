# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0013_auto_20150521_0949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='store',
            options={'ordering': ('region__name', 'location')},
        ),
        migrations.AddField(
            model_name='store',
            name='reference_name',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
    ]
