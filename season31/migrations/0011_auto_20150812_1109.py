# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0010_auto_20150727_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='castawayepisode',
            old_name='has_score_changed',
            new_name='score_has_changed',
        ),
        migrations.RenameField(
            model_name='playerepisode',
            old_name='has_score_changed',
            new_name='score_has_changed',
        ),
    ]
