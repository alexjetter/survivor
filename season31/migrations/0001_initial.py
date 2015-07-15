# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('score', models.IntegerField(default=1)),
                ('icon_filename', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Castaway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('full_name', models.CharField(max_length=32)),
                ('age', models.PositiveIntegerField(default=0)),
                ('occupation', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='CastawayEpisode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('actions', models.ManyToManyField(to='season31.Action', blank=True)),
                ('castaway', models.ForeignKey(to='season31.Castaway')),
            ],
            options={
                'ordering': ('episode', 'tribe', 'castaway'),
                'get_latest_by': 'episode',
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('number', models.PositiveIntegerField(default=0)),
                ('air_date', models.DateTimeField()),
                ('team_size', models.PositiveIntegerField(default=5)),
                ('castaways', models.ManyToManyField(to='season31.Castaway', through='season31.CastawayEpisode')),
            ],
            options={
                'ordering': ('number',),
                'get_latest_by': 'air_date',
            },
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'TM', max_length=2, choices=[(b'TM', b'Team Member'), (b'VO', b'Vote Off')])),
                ('castaway_episode', models.ForeignKey(to='season31.CastawayEpisode')),
            ],
            options={
                'ordering': ('castaway_episode', 'type', 'player_episode'),
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paid', models.BooleanField(default=False)),
                ('score', models.PositiveIntegerField(default=0)),
                ('place', models.PositiveIntegerField(default=0)),
                ('movement', models.IntegerField(default=0)),
                ('show_league_only', models.BooleanField(default=False)),
                ('league', models.ForeignKey(blank=True, to='season31.League', null=True)),
            ],
            options={
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='PlayerEpisode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_score', models.PositiveIntegerField(default=0)),
                ('vote_off_score', models.PositiveIntegerField(default=0)),
                ('jsp_score', models.PositiveIntegerField(default=0)),
                ('week_score', models.PositiveIntegerField(default=0)),
                ('total_score', models.PositiveIntegerField(default=0)),
                ('place', models.PositiveIntegerField(default=0)),
                ('movement', models.IntegerField(default=0)),
                ('actions', models.ManyToManyField(to='season31.Action', blank=True)),
                ('episode', models.ForeignKey(to='season31.Episode')),
                ('player', models.ForeignKey(to='season31.Player')),
            ],
            options={
                'ordering': ('episode', 'player'),
                'get_latest_by': 'episode',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('number', models.PositiveIntegerField(default=0)),
                ('air_date', models.DateTimeField()),
            ],
            options={
                'ordering': ('number',),
                'get_latest_by': 'air_date',
            },
        ),
        migrations.CreateModel(
            name='Tribe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('color', models.CharField(max_length=32)),
                ('season', models.ForeignKey(blank=True, to='season31.Season', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_ftc_vote', models.BooleanField(default=False)),
                ('castaway', models.ForeignKey(to='season31.Castaway')),
                ('castaway_episode', models.ForeignKey(to='season31.CastawayEpisode')),
            ],
            options={
                'ordering': ('castaway_episode', 'castaway'),
            },
        ),
        migrations.AddField(
            model_name='player',
            name='season',
            field=models.ForeignKey(blank=True, to='season31.Season', null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pick',
            name='player_episode',
            field=models.ForeignKey(to='season31.PlayerEpisode'),
        ),
        migrations.AddField(
            model_name='league',
            name='season',
            field=models.ForeignKey(blank=True, to='season31.Season', null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='players',
            field=models.ManyToManyField(to='season31.Player', through='season31.PlayerEpisode'),
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(blank=True, to='season31.Season', null=True),
        ),
        migrations.AddField(
            model_name='castawayepisode',
            name='episode',
            field=models.ForeignKey(to='season31.Episode'),
        ),
        migrations.AddField(
            model_name='castawayepisode',
            name='tribe',
            field=models.ForeignKey(to='season31.Tribe'),
        ),
        migrations.AddField(
            model_name='castaway',
            name='season',
            field=models.ForeignKey(blank=True, to='season31.Season', null=True),
        ),
    ]
