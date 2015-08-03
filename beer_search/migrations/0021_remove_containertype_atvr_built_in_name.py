# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0020_containertype_atvr_built_in_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='containertype',
            name='atvr_built_in_name',
        ),
    ]
