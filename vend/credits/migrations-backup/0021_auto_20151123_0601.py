# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0020_userprofile_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='area',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='design',
            name='volume',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
