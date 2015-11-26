# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0033_auto_20151120_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='UntappdStyle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='', blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
