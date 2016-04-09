# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0013_design_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='cost',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
