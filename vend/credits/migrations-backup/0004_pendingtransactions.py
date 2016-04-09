# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('credits', '0003_auto_20151021_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingTransactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('processed', models.BooleanField(default=False)),
                ('purchased', models.ForeignKey(to='credits.Purchase')),
                ('purchaser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
