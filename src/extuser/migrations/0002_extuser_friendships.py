# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 23:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friendship', '0001_initial'),
        ('extuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extuser',
            name='friendships',
            field=models.ManyToManyField(related_name='_extuser_friendships_+', through='friendship.Friendship', to=settings.AUTH_USER_MODEL),
        ),
    ]