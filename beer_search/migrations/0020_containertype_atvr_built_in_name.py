# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0019_modifiablesettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='containertype',
            name='atvr_built_in_name',
            field=models.CharField(max_length=50, default='FL.'),
            preserve_default=False,
        ),
    ]
