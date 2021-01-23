# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0014_auto_20201007_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='speaking',
        ),
    ]
