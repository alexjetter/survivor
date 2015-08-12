# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0003_auto_20150720_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('league', models.ForeignKey(to='season31.League')),
            ],
            options={
                'ordering': ('league',),
            },
        ),
        migrations.CreateModel(
            name='PlayerEpisodePlacement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('place', models.PositiveIntegerField(default=0)),
                ('movement', models.IntegerField(default=0)),
                ('leaderboard', models.ForeignKey(to='season31.Leaderboard')),
                ('player_episode', models.ForeignKey(to='season31.PlayerEpisode')),
            ],
            options={
                'ordering': ('place',),
            },
        ),
        migrations.RemoveField(
            model_name='player',
            name='movement',
        ),
        migrations.RemoveField(
            model_name='player',
            name='place',
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='players',
            field=models.ManyToManyField(to='season31.Player'),
        ),
    ]
