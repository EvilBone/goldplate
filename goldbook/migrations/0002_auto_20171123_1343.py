# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goldbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_pub_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='出版日期'),
        ),
    ]
