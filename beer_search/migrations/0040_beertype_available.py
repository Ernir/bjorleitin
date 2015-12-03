# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0039_simplifiedstyle_html_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='beertype',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
