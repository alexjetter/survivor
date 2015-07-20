# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='castaway',
            name='season',
        ),
        migrations.RemoveField(
            model_name='episode',
            name='season',
        ),
        migrations.RemoveField(
            model_name='league',
            name='season',
        ),
        migrations.RemoveField(
            model_name='player',
            name='season',
        ),
        migrations.RemoveField(
            model_name='tribe',
            name='season',
        ),
        migrations.AddField(
            model_name='castawayepisode',
            name='has_score_changed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playerepisode',
            name='has_score_changed',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Season',
        ),
    ]
