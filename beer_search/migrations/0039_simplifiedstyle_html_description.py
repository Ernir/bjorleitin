# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0038_simplifiedstyle_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplifiedstyle',
            name='html_description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
