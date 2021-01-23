# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0011_auto_20201006_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='answers',
            field=models.FileField(blank=True, upload_to='answers'),
        ),
    ]
