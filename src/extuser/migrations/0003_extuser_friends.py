# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-26 11:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friendship', '0003_auto_20161026_1124'),
        ('extuser', '0002_extuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='extuser',
            name='friends',
            field=models.ManyToManyField(through='friendship.Friendship', to=settings.AUTH_USER_MODEL),
        ),
    ]
