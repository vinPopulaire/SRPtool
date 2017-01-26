# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-26 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20170126_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserContentScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=3, max_digits=6)),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Term')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
            options={
                'verbose_name': 'UserContentScore',
                'verbose_name_plural': 'UserContentScores',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='score',
            field=models.ManyToManyField(through='api.UserContentScore', to='api.Term'),
        ),
    ]
