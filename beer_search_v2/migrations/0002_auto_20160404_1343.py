# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name', 'container__name', 'volume')},
        ),
        migrations.RenameField(
            model_name='untappdentity',
            old_name='untappd_style',
            new_name='style',
        ),
        migrations.RemoveField(
            model_name='brewery',
            name='untappd_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='new',
        ),
        migrations.RemoveField(
            model_name='producttype',
            name='untappd_id',
        ),
        migrations.RemoveField(
            model_name='producttype',
            name='untappd_rating',
        ),
        migrations.RemoveField(
            model_name='untappdentity',
            name='product_type',
        ),
        migrations.AddField(
            model_name='producttype',
            name='untappd_info',
            field=models.ForeignKey(to='beer_search_v2.UntappdEntity', null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='untappdentity',
            name='rating',
            field=models.FloatField(null=True, blank=True, default=None),
        ),
        migrations.AddField(
            model_name='untappdentity',
            name='untappd_id',
            field=models.IntegerField(unique=True, default=1),
            preserve_default=False,
        ),
    ]
