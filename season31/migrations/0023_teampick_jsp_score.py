# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0022_player_forgot_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='teampick',
            name='jsp_score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
