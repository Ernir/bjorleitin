# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0021_remove_containertype_atvr_built_in_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='first_seen_at',
            field=models.DateTimeField(null=True),
        ),
    ]
