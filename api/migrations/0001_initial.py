# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-07 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Age',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Ages',
                'verbose_name': 'Age',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Genders',
                'verbose_name': 'Gender',
            },
        ),
    ]
