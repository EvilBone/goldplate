# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goldbook', '0009_auto_20171128_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlmanager',
            name='web_url',
            field=models.CharField(max_length=500, verbose_name='URL'),
        ),
    ]
