# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import registrar.models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0008_auto_20200930_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendhomework',
            name='file',
            field=models.FileField(upload_to=registrar.models.PathAndRename('students/homework')),
        ),
    ]
