# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-29 02:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extuser',
            name='avatar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermedia.Photo'),
        ),
    ]