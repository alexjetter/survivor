# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0014_player_show_help_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamPick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('castaway', models.ForeignKey(to='season31.Castaway')),
                ('episode', models.ForeignKey(to='season31.Episode')),
                ('player', models.ForeignKey(to='season31.Player')),
            ],
            options={
                'ordering': ('episode', 'player', 'castaway'),
            },
        ),
        migrations.CreateModel(
            name='VotePick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('castaway', models.ForeignKey(to='season31.Castaway')),
                ('episode', models.ForeignKey(to='season31.Episode')),
                ('player', models.ForeignKey(to='season31.Player')),
            ],
            options={
                'ordering': ('episode', 'player', 'castaway'),
            },
        ),
        migrations.RemoveField(
            model_name='pick',
            name='castaway_episode',
        ),
        migrations.RemoveField(
            model_name='pick',
            name='player_episode',
        ),
        migrations.DeleteModel(
            name='Pick',
        ),
    ]
