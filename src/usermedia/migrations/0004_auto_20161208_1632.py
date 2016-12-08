# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-08 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import usermedia.models


class Migration(migrations.Migration):

    dependencies = [
        ('usermedia', '0003_auto_20161208_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='photo',
        ),
        migrations.AddField(
            model_name='photo',
            name='file',
            field=models.FileField(default='', upload_to=usermedia.models.upload_photos),
        ),
    ]