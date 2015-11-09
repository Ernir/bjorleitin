# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0024_auto_20151101_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftBox',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('abv', models.FloatField()),
                ('price', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('atvr_id', models.CharField(max_length=5)),
                ('first_seen_at', models.DateTimeField(null=True)),
                ('available', models.BooleanField(default=True)),
                ('temporary', models.BooleanField(default=False)),
                ('new', models.BooleanField(default=False)),
                ('country', models.ForeignKey(default=None, to='beer_search.Country', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
