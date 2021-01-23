# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0012_homework_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='speaking',
            field=models.FileField(blank=True, upload_to='speaking'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='file',
            field=models.FileField(blank=True, upload_to='homeworks'),
        ),
    ]
