# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0041_beertype_needs_announcement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplifiedstyle',
            name='description',
            field=models.TextField(null=True, default='', blank=True),
        ),
    ]
