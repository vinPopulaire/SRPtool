# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-12 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='annotations',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='video',
            name='path',
            field=models.CharField(default='unknown', max_length=150),
        ),
        migrations.AddField(
            model_name='video',
            name='source',
            field=models.CharField(default='unknown', max_length=150),
        ),
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='video',
            name='genre',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='video',
            name='geographical_coverage',
            field=models.CharField(default='unknown', max_length=150),
        ),
        migrations.AlterField(
            model_name='video',
            name='thesaurus_terms',
            field=models.CharField(default='unknown', max_length=250),
        ),
        migrations.AlterField(
            model_name='video',
            name='topic',
            field=models.CharField(default='unknown', max_length=150),
        ),
    ]
