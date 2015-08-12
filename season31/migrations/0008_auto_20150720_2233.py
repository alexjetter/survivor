# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0007_auto_20150720_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='players',
        ),
        migrations.AddField(
            model_name='player',
            name='leagues',
            field=models.ManyToManyField(to='season31.League', blank=True),
        ),
    ]
