# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0002_auto_20150720_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerepisode',
            name='actions',
        ),
        migrations.AddField(
            model_name='playerepisode',
            name='correctly_predicted_votes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
