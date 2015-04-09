# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0004_auto_20150409_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beer',
            name='style',
        ),
        migrations.AddField(
            model_name='beer',
            name='style',
            field=models.ForeignKey(to='beer_search.Style', default=None, null=True),
        ),
    ]
