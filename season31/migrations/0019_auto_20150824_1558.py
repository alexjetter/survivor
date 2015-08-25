# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season31', '0018_action_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='castaway',
            options={'ordering': ('place', 'tribe_name', 'name')},
        ),
        migrations.AddField(
            model_name='castaway',
            name='tribe_name',
            field=models.CharField(default='PlaceholdeR', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tribe',
            name='color',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='tribe',
            name='name',
            field=models.CharField(max_length=16),
        ),
    ]
