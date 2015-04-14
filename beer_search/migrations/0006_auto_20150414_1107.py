# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0005_auto_20150409_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beer',
            options={'ordering': ('name', 'container__name')},
        ),
        migrations.AddField(
            model_name='style',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='style',
            name='simplifies_to',
            field=models.ForeignKey(to='beer_search.Style', blank=True, null=True),
        ),
    ]
