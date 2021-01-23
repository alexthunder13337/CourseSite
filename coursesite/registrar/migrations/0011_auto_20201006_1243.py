# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('registrar', '0010_auto_20201001_0304'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tier1_students',
            field=models.ManyToManyField(blank=True, null=True, related_name='tier1', to='account.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='tier2_students',
            field=models.ManyToManyField(blank=True, null=True, related_name='tier2', to='account.Student'),
        ),
    ]
