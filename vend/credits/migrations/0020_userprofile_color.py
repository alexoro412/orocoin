# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0019_design_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='color',
            field=models.CharField(default=b'blue-grey', max_length=40),
            preserve_default=True,
        ),
    ]
