# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0030_beercategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beercategory',
            options={'ordering': ('name',), 'verbose_name_plural': 'beer categories'},
        ),
        migrations.AddField(
            model_name='beercategory',
            name='boxes',
            field=models.ManyToManyField(to='beer_search.GiftBox'),
        ),
        migrations.AddField(
            model_name='beercategory',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
