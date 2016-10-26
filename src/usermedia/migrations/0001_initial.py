# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 00:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import usermedia.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('name', models.CharField(default=None, max_length=40, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.CharField(default=None, max_length=255, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_comments', models.PositiveIntegerField(default=0, verbose_name='\u0427\u0438\u0441\u043b\u043e \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0435\u0432')),
                ('count_likes', models.PositiveIntegerField(default=0, verbose_name='\u0427\u0438\u0441\u043b\u043e \u043b\u0430\u0439\u043a\u043e\u0432')),
                ('preview', models.BooleanField(default=False, verbose_name='\u041f\u0440\u0435\u0432\u044c\u044e')),
                ('description', models.CharField(default=None, max_length=255, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('added_at', models.DateField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=usermedia.models.upload_photos, verbose_name='\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u044f')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermedia.Album')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]