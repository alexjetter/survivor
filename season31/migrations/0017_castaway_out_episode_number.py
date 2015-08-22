# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0016_castaway_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='castaway',
            name='out_episode_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
