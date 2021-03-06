# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-19 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_term'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrichment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrichment_id', models.CharField(max_length=50, unique=True)),
                ('enrichment_class', models.CharField(max_length=50)),
                ('longName', models.CharField(max_length=250)),
                ('dbpediaURL', models.CharField(max_length=150)),
                ('wikipediaURL', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('thumbnail', models.CharField(max_length=150)),
                ('time_added', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Enrichments',
                'verbose_name': 'Enrichment',
            },
        ),
    ]
