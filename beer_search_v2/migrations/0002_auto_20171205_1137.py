# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-05 11:37
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search_v2', '0001_squashed_0038_delete_mainqueryresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='ATVRProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('atvr_id', models.CharField(max_length=100)),
                ('price', models.IntegerField(null=True)),
                ('volume', models.IntegerField(null=True)),
                ('container', models.CharField(choices=[('DS.', 'Dós'), ('FL.', 'Flaska'), ('KÚT', 'Kútur'), ('ASKJA', 'Gjafaaskja'), ('ANNAD', 'Ótilgreint')], max_length=5)),
                ('first_seen_at', models.DateTimeField(null=True)),
                ('available_in_atvr', models.BooleanField(default=False)),
                ('temporary', models.BooleanField(default=False)),
                ('atvr_stock', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
                ('updated_at', models.DateField(default=datetime.date.today)),
                ('image_url', models.URLField(blank=True, default='')),
                ('untappd_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='beer_search_v2.UntappdEntity')),
            ],
            options={
                'ordering': ('name', 'container', 'volume'),
            },
        ),
        migrations.AlterField(
            model_name='productlist',
            name='description',
            field=models.TextField(),
        ),
    ]