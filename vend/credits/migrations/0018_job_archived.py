# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0017_accept'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='archived',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
