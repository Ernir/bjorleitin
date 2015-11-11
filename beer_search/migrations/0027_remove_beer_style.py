# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0026_auto_20151109_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beer',
            name='style',
        ),
    ]
