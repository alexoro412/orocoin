# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0006_remove_pendingtransactions_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingtransactions',
            name='item',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
