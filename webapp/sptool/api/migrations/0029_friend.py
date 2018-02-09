# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-09 10:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20170629_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to='api.User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='api.User')),
            ],
            options={
                'verbose_name': 'Friend',
                'verbose_name_plural': 'Friends',
            },
        ),
    ]
