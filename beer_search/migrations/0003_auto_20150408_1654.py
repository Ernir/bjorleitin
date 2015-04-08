# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beer_search', '0002_auto_20150408_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterModelOptions(
            name='beer',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='beer',
            name='container',
            field=models.ForeignKey(null=True, to='beer_search.ContainerType'),
        ),
    ]
