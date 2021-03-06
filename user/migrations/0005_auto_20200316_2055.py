# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-16 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200312_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='max_dating_age',
            field=models.IntegerField(default=80, verbose_name='最大交友年龄'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='min_dating_age',
            field=models.IntegerField(default=16, verbose_name='最小交友年龄'),
        ),
    ]
