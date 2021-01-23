# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0005_auto_20200919_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
