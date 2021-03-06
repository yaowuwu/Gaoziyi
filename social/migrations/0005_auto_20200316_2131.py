# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-16 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20200316_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swiper',
            name='stime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='滑动时间'),
        ),
        migrations.AlterField(
            model_name='swiper',
            name='stype',
            field=models.CharField(choices=[('superlike', '上滑'), ('like', '右滑'), ('dislike', '左滑')], max_length=16, verbose_name='滑动的类型'),
        ),
    ]
