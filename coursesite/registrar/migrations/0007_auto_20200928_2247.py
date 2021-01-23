# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0006_auto_20200927_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendhomework',
            name='file',
            field=models.FileField(upload_to='student_homework'),
        ),
    ]
