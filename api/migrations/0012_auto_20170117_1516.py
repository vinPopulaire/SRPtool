# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-17 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20170117_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='geographical_coverage',
            field=models.CharField(max_length=150),
        ),
    ]