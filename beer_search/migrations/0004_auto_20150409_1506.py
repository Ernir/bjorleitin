# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0003_auto_20150408_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='updated_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='beer',
            name='container',
            field=models.ForeignKey(to='beer_search.ContainerType', null=True, default=None),
        ),
    ]
