# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-26 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_enrichmentcontentscore'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Watched',
            new_name='VideoWatched',
        ),
        migrations.AlterModelOptions(
            name='videowatched',
            options={'verbose_name': 'VideoWatched', 'verbose_name_plural': 'VideoWatcheds'},
        ),
        migrations.RenameField(
            model_name='video',
            old_name='scores',
            new_name='score',
        ),
        migrations.RenameField(
            model_name='videointeractions',
            old_name='watched',
            new_name='video_watched',
        ),
        migrations.RemoveField(
            model_name='video',
            name='users',
        ),
        migrations.AddField(
            model_name='user',
            name='video',
            field=models.ManyToManyField(through='api.VideoWatched', to='api.Video'),
        ),
    ]
