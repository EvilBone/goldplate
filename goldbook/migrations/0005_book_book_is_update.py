# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goldbook', '0004_auto_20171123_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_is_update',
            field=models.BooleanField(default=False, verbose_name='是否更新'),
        ),
    ]
