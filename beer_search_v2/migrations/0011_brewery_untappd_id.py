# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0010_auto_20160417_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='brewery',
            name='untappd_id',
            field=models.IntegerField(unique=True, default=0),
            preserve_default=False,
        ),
    ]
