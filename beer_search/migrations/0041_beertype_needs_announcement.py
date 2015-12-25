# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0040_beertype_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='beertype',
            name='needs_announcement',
            field=models.BooleanField(default=False),
        ),
    ]
