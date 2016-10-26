# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from enum import Enum


# Create your models here.


class Friendship(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver')

    class Meta:
        unique_together = ("sender", "receiver")
