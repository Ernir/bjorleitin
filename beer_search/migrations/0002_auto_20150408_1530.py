# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('abv', models.FloatField()),
                ('price', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('atvr_id', models.CharField(max_length=5)),
            ],
        ),
        migrations.RenameModel(
            old_name='BeerCategory',
            new_name='Style',
        ),
        migrations.AddField(
            model_name='beer',
            name='style',
            field=models.ManyToManyField(to='beer_search.Style'),
        ),
    ]
