# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=500)),
                ('untappd_id', models.IntegerField(unique=True)),
                ('alias', models.CharField(null=True, max_length=500, blank=True)),
            ],
            options={
                'verbose_name_plural': 'breweries',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ContainerType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'countries',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('product_id', models.CharField(max_length=100, unique=True)),
                ('first_seen_at', models.DateTimeField(null=True)),
                ('available', models.BooleanField(default=True)),
                ('temporary', models.BooleanField(default=False)),
                ('new', models.BooleanField(default=False)),
                ('updated_at', models.DateField(default=datetime.date.today)),
                ('container', models.ForeignKey(to='beer_search_v2.ContainerType')),
            ],
            options={
                'ordering': ('name', 'container__name'),
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('abv', models.FloatField()),
                ('untappd_id', models.IntegerField(null=True, blank=True, default=None)),
                ('untappd_rating', models.FloatField(null=True, blank=True, default=None)),
                ('available', models.BooleanField(default=False)),
                ('needs_announcement', models.BooleanField(default=False)),
                ('country', models.ForeignKey(null=True, to='beer_search_v2.Country', blank=True, default=None)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SimplifiedStyle',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(null=True, blank=True, default='')),
                ('html_description', models.TextField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='UntappdEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('brewery', models.ForeignKey(null=True, to='beer_search_v2.Brewery', blank=True, default=None)),
                ('product_type', models.ForeignKey(to='beer_search_v2.ProductType')),
            ],
        ),
        migrations.CreateModel(
            name='UntappdStyle',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('simplifies_to', models.ForeignKey(null=True, to='beer_search_v2.SimplifiedStyle')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='untappdentity',
            name='untappd_style',
            field=models.ForeignKey(null=True, to='beer_search_v2.UntappdStyle', blank=True, default=None),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(to='beer_search_v2.ProductType'),
        ),
    ]
