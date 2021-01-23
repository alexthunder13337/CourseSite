# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0016_remove_homework_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='answers',
            field=models.FileField(blank=True, null=True, upload_to='answers'),
        ),
        migrations.AddField(
            model_name='homework',
            name='speaking',
            field=models.FileField(blank=True, null=True, upload_to='speaking'),
        ),
    ]
