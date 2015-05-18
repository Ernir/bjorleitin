# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0011_auto_20150518_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='country',
            field=models.ForeignKey(default=None, to='beer_search.Country', null=True),
        ),
    ]
