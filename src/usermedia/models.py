# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from useractivities.models import BaseEvent, WithLike, WithComment


class Album(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1
    )

    created_at = models.DateField(
        u'Дата создания',
        auto_now_add=True
    )

    name = models.CharField(
        u'Название',
        max_length=40,
        default=None
    )

    description = models.CharField(
        u'Описание',
        max_length=255,
        default=None
    )


def upload_photos(obj, filename):
    to = obj.album.user.email + "/" + "photo" + "/" + filename
    return to


class Photo(BaseEvent, WithLike, WithComment):
    user = None
    album = models.ForeignKey(Album)

    preview = models.BooleanField(
        u'Превью',
        default=False
    )

    description = models.CharField(
        u'Описание',
        max_length=255,
        default=None
    )

    added_at = models.DateField(
        u'Дата добавления',
        auto_now_add=True
    )

    photo = models.FileField(
        upload_to=upload_photos,
        default=''
    )

    class Meta:
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'
        abstract = False

    def get_event_name(self):
        return "%s %s добавил новую фотографию в альбом %s " % (
            self.album.user.firstname, self.album.user.lastname, self.album.name)

    def get_event_author(self):
        return self.album.user
