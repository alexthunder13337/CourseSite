# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0013_auto_20201007_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='answers',
            field=models.FileField(blank=True, null=True, upload_to='answers'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='homeworks'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='speaking',
            field=models.FileField(blank=True, null=True, upload_to='speaking'),
        ),
    ]
