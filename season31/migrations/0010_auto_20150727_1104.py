# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0009_auto_20150727_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerepisode',
            name='movement',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerepisode',
            name='place',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerepisode',
            name='action_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerepisode',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerepisode',
            name='week_score',
            field=models.IntegerField(default=0),
        ),
    ]
