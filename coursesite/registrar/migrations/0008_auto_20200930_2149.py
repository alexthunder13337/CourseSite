# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import registrar.models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0007_auto_20200928_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='week_num',
        ),
        migrations.AlterField(
            model_name='sendhomework',
            name='file',
            field=models.FileField(upload_to=registrar.models.PathAndRename('/students/homework')),
        ),
    ]
