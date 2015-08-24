# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0017_castaway_out_episode_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='description',
            field=models.CharField(default='dummy text', max_length=64),
            preserve_default=False,
        ),
    ]
