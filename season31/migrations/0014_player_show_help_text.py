# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0013_episode_is_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='show_help_text',
            field=models.BooleanField(default=True),
        ),
    ]
