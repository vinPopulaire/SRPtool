# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-28 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20170222_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
