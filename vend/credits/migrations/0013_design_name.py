# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0012_design'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='name',
            field=models.CharField(default=uuid.uuid4, unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
