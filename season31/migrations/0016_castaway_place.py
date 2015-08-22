# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0015_auto_20150819_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='castaway',
            name='place',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
