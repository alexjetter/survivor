# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0011_auto_20150812_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerepisode',
            name='loyalty_bonus',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
