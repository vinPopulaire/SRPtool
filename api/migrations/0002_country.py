# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-08 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Countrys',
                'verbose_name': 'Country',
            },
        ),
    ]
