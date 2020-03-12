# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-12 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='dating_sex',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='uid',
        ),
        migrations.AddField(
            model_name='profile',
            name='dating_gender',
            field=models.CharField(choices=[('male', '男性'), ('female', '女性')], default='female', max_length=10, verbose_name='匹配的性别'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dating_location',
            field=models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('深圳', '深圳'), ('郑州', '郑州'), ('西安', '西安'), ('武汉', '武汉'), ('成都', '成都'), ('沈阳', '沈阳')], default='北京', max_length=10, verbose_name='目标城市'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='max_distance',
            field=models.IntegerField(default=60, max_length=64, verbose_name='最大查找范围'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='min_distance',
            field=models.IntegerField(default=1, max_length=64, verbose_name='最小查找范围'),
        ),
    ]
