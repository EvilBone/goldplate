# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goldbook', '0005_book_book_is_update'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_is_update',
            new_name='book_is_update_dd',
        ),
        migrations.AddField(
            model_name='book',
            name='book_is_update_jd',
            field=models.BooleanField(default=False, verbose_name='是否更新'),
        ),
    ]