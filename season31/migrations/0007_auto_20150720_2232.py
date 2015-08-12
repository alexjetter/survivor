# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0006_auto_20150720_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='leagues',
        ),
        migrations.AddField(
            model_name='league',
            name='players',
            field=models.ManyToManyField(to='season31.Player', blank=True),
        ),
    ]
