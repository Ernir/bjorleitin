# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0022_beer_first_seen_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beer',
            old_name='seasonal',
            new_name='temporary',
        ),
        migrations.AlterField(
            model_name='beer',
            name='new',
            field=models.BooleanField(default=False),
        ),
    ]
