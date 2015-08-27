# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0020_auto_20150827_1452'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('username',)},
        ),
    ]
