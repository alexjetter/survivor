# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0019_auto_20150824_1558'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ('-score', 'name')},
        ),
        migrations.AlterModelOptions(
            name='castawayepisode',
            options={'ordering': ('episode', 'tribe', '-score', 'castaway'), 'get_latest_by': 'episode'},
        ),
        migrations.AddField(
            model_name='player',
            name='username',
            field=models.CharField(default=b'', max_length=32),
        ),
    ]
