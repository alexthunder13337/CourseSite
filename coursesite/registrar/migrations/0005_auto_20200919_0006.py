# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0004_auto_20200918_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homework',
            name='file',
            field=models.FileField(upload_to='homeworks'),
        ),
    ]
