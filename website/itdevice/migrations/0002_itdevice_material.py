# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itdevice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Itdevice',
            fields=[
                ('itdevice_id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('pur_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'itdevice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('material_id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('materialname', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'material',
                'managed': False,
            },
        ),
    ]