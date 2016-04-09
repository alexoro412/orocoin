# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0016_auto_20151104_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.ForeignKey(to='credits.Job')),
                ('submission', models.ForeignKey(to='credits.Submission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
