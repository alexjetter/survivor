# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0024_auto_20150910_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='score_jsps',
            field=models.BooleanField(default=False),
        ),
    ]
