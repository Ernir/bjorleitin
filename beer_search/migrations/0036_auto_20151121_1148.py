# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0035_beertype_untappd_style'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimplifiedStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='', blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='untappdstyle',
            name='simplifies_to',
            field=models.ForeignKey(to='beer_search.SimplifiedStyle', null=True),
        ),
    ]
