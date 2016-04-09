# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0008_remove_pendingtransactions_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingtransactions',
            name='identifier',
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
