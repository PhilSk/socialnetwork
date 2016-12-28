# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-26 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import useractivities.models


class Migration(migrations.Migration):

    dependencies = [
        ('useractivities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='attachment',
            field=models.FileField(upload_to=useractivities.models.upload_attachments),
        ),
    ]