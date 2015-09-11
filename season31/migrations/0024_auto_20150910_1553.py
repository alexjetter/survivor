# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0023_teampick_jsp_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='castawayepisode',
            name='score_has_changed',
        ),
        migrations.RemoveField(
            model_name='playerepisode',
            name='score_has_changed',
        ),
    ]
