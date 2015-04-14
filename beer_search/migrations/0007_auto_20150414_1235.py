# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0006_auto_20150414_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='beer',
            name='new',
            field=models.BooleanField(default=True),
        ),
    ]
