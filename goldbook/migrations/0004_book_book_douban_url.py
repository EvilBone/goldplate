# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goldbook', '0003_auto_20171121_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_douban_url',
            field=models.URLField(default='', verbose_name='豆瓣链接'),
        ),
    ]