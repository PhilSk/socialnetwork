from __future__ import unicode_literals

from django.conf import settings
from django.db import models


# Create your models here.

class Chat(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.name)


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    chat = models.ForeignKey(Chat)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str("Message: " + self.text)
