# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0037_remove_untappdstyle_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplifiedstyle',
            name='slug',
            field=models.SlugField(max_length=100, default=''),
            preserve_default=False,
        ),
    ]
