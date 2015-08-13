# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0012_playerepisode_loyalty_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]
