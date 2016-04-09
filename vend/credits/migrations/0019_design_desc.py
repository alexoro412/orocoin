# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0018_job_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='desc',
            field=models.CharField(default='', max_length=140),
            preserve_default=False,
        ),
    ]
