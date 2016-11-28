# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.db import models


# Create your models here.
from useractivities.models import BaseEvent


class Friendship(BaseEvent):
    user = None
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver')

    class Meta:
        unique_together = ("sender", "receiver")
        abstract = False

    def get_event_name(self):
        return "%d и %d теперь друзья" % (self.sender, self.receiver)

    def get_event_author(self):
        return self.sender
