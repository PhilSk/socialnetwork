# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from useractivities.models import BaseEvent
from django.utils.translation import ugettext as _l


class Friendship(BaseEvent):
    user = None
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver')

    class Meta:
        unique_together = ("sender", "receiver")
        abstract = False

    def get_event_name(self):
        umodel = get_user_model()
        sender_user = self.sender
        receiver_user = self.receiver
        if not isinstance(self.sender, umodel) or not isinstance(self.receiver, umodel):
            sender_user = umodel.objects.get(id=self.sender)
            receiver_user = umodel.objects.get(id=self.receiver)
        return _l(u"%s %s и %s %s теперь друзья") % (
            sender_user.firstname, sender_user.lastname, receiver_user.firstname, receiver_user.lastname)

    def get_event_author(self):
        return self.sender
