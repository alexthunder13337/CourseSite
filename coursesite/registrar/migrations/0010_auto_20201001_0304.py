# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0009_auto_20200930_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='finish_date',
        ),
        migrations.RemoveField(
            model_name='course',
            name='start_date',
        ),
    ]
