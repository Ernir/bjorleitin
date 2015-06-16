# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0017_beer_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beer',
            old_name='type',
            new_name='beer_type',
        ),
    ]
