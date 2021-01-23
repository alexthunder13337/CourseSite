# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('hw_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=127)),
                ('file', models.FileField(upload_to='/homeworks')),
            ],
            options={
                'db_table': 'at_homeworks',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('lesson_id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson_num', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(max_length=127)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'at_lessons',
            },
        ),
        migrations.CreateModel(
            name='SendHomework',
            fields=[
                ('student_hw_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='/student_homework')),
                ('comment', models.CharField(max_length=255)),
                ('lesson', models.ForeignKey(to='registrar.Lesson')),
                ('student', models.ForeignKey(to='account.Student')),
            ],
            options={
                'db_table': 'at_students_hw',
            },
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='bliptv_url',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='course',
        ),
        migrations.AddField(
            model_name='lecture',
            name='videofile',
            field=models.FileField(null=True, upload_to='lectures/', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='coursesubmission',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='notes',
            field=models.ManyToManyField(to='registrar.FileUpload', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='preferred_service',
            field=models.CharField(default='4', choices=[('1', 'YouTube'), ('2', 'Vimeo'), ('4', 'EMPlayer')], max_length=1),
        ),
        migrations.AddField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(to='registrar.Course'),
        ),
        migrations.AddField(
            model_name='homework',
            name='Lesson',
            field=models.ForeignKey(to='registrar.Lesson'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='lesson',
            field=models.ForeignKey(null=True, to='registrar.Lesson'),
        ),
    ]
