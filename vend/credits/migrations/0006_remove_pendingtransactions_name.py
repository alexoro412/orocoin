# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0005_pendingtransactions_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendingtransactions',
            name='name',
        ),
    ]
