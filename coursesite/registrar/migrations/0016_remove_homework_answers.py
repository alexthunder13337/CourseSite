# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0015_remove_homework_speaking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='answers',
        ),
    ]
