# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-26 11:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_videointeractions_computed'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnrichmentContentScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=3, max_digits=6)),
                ('enrichment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Enrichment')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Term')),
            ],
            options={
                'verbose_name_plural': 'EnrichmentContentScores',
                'verbose_name': 'EnrichmentContentScore',
            },
        ),
    ]
