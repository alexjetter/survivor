# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0021_auto_20150827_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='forgot_password',
            field=models.BooleanField(default=False),
        ),
    ]
