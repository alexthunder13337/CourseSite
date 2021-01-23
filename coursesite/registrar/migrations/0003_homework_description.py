# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_auto_20200918_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='description',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
    ]
