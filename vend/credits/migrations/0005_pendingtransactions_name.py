# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0004_pendingtransactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingtransactions',
            name='name',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
