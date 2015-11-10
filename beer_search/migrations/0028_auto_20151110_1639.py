# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0027_remove_beer_style'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('untappd_id', models.IntegerField(unique=True)),
                ('alias', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='beer',
            name='country',
        ),
        migrations.AddField(
            model_name='beertype',
            name='brewery',
            field=models.ForeignKey(to='beer_search.Brewery', default=None, null=True),
        ),
    ]
