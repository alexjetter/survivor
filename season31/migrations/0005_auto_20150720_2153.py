# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0004_auto_20150720_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaguePlayerEpisode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('place', models.PositiveIntegerField(default=0)),
                ('movement', models.IntegerField(default=0)),
                ('episode', models.ForeignKey(to='season31.Episode')),
                ('league', models.ForeignKey(to='season31.League')),
                ('player', models.ForeignKey(to='season31.Player')),
            ],
            options={
                'ordering': ('league', 'player', 'episode'),
            },
        ),
        migrations.RemoveField(
            model_name='leaderboard',
            name='league',
        ),
        migrations.RemoveField(
            model_name='leaderboard',
            name='players',
        ),
        migrations.RemoveField(
            model_name='playerepisodeplacement',
            name='leaderboard',
        ),
        migrations.RemoveField(
            model_name='playerepisodeplacement',
            name='player_episode',
        ),
        migrations.DeleteModel(
            name='Leaderboard',
        ),
        migrations.DeleteModel(
            name='PlayerEpisodePlacement',
        ),
    ]
