# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0008_auto_20150720_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leagueplayerepisode',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='leagueplayerepisode',
            name='league',
        ),
        migrations.RemoveField(
            model_name='leagueplayerepisode',
            name='player',
        ),
        migrations.RemoveField(
            model_name='player',
            name='leagues',
        ),
        migrations.RemoveField(
            model_name='player',
            name='score',
        ),
        migrations.RemoveField(
            model_name='player',
            name='show_league_only',
        ),
        migrations.RemoveField(
            model_name='playerepisode',
            name='movement',
        ),
        migrations.RemoveField(
            model_name='playerepisode',
            name='place',
        ),
        migrations.AddField(
            model_name='player',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='League',
        ),
        migrations.DeleteModel(
            name='LeaguePlayerEpisode',
        ),
    ]
