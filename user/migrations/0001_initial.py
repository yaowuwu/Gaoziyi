# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-10 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=15, verbose_name='手机号')),
                ('nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('gender', models.CharField(choices=[('male', '男性'), ('female', '女性')], default='male', max_length=10, verbose_name='性别')),
                ('birthday', models.DateField(default='2000-01-01', verbose_name='生日')),
                ('avatar', models.CharField(max_length=256, verbose_name='个人形象的URL')),
                ('location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('深圳', '深圳'), ('郑州', '郑州'), ('西安', '西安'), ('武汉', '武汉'), ('成都', '成都'), ('沈阳', '沈阳')], max_length=10, verbose_name='常居地')),
            ],
        ),
    ]
