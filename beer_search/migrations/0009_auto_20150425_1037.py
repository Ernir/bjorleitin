# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0008_remove_style_simplifies_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='seasonal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='beer',
            name='suffix',
            field=models.CharField(max_length=100, default=''),
        ),
    ]
