# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0002_auto_20160404_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlcoholCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('alias', models.CharField(null=True, max_length=200, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='producttype',
            name='alias',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='producttype',
            name='alcohol_category',
            field=models.ForeignKey(null=True, to='beer_search_v2.AlcoholCategory', default=None),
        ),
    ]
