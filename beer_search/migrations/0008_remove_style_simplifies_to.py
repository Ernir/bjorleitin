# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0007_auto_20150414_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='style',
            name='simplifies_to',
        ),
    ]
