# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0010_auto_20151022_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingtransactions',
            name='purchaser',
            field=models.ForeignKey(related_name=b'purchases', to=settings.AUTH_USER_MODEL),
        ),
    ]
