# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from useractivities.signals import base_event_post_save, like_up, comment_up
from usermedia.models import WithLike, WithComment, WithContentType


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = u'Лайк'
        verbose_name_plural = u'Лайки'


class BaseEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1
    )

    def get_event_name(self):
        return self.name

    def get_event_author(self):
        return self.user

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'
        abstract = True


class Post(BaseEvent, WithComment, WithLike):
    title = models.CharField(
        u'Заголовок поста',
        max_length=255
    )

    content = models.TextField(
        u'Текст поста',
        default=None
    )

    created_at = models.DateTimeField(
        u'Создан',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        u'Обновлен',
        auto_now=True
    )

    class Meta:
        verbose_name = u'Пост'
        verbose_name_plural = u'Посты'
        abstract = False

    def get_event_name(self):
        return "Новый пост от пользователя %s: %s" % (self.user, self.title)

    def get_event_author(self):
        return self.user


class Comment(BaseEvent, WithLike):
    content = models.CharField(
        u'Текст комментария',
        default=None,
        max_length=255
    )

    created_at = models.DateTimeField(
        u'Создан',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        u'Обновлен',
        auto_now=True
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
        abstract = False

    def get_event_name(self):
        return "Новый комментарий"

    def get_event_author(self):
        return self.user


class Meeting(BaseEvent):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participants"
    )

    description = models.TextField(
        u'Описание',
        default=u'Создатель события, увы, ещё не оставил его описания'
    )

    duration = models.TimeField(
        u'Длительность мероприятия',
        default=None
    )

    when = models.DateTimeField(
        u'Когда',
        default=None
    )

    class Meta:
        verbose_name = u'Встреча'
        verbose_name_plural = u'Встречи'
        abstract = False

    def get_event_name(self):
        return self.description[100:] + "..."

    def get_event_author(self):
        return self.user


class Birthday(BaseEvent):
    when = models.DateTimeField(
        u'Когда',
        default=None
    )

    class Meta:
        verbose_name = u'День рождения'
        verbose_name_plural = u'Дни рождения'
        abstract = False

    def get_event_name(self):
        return "Сегодня день рождения у %d" % self.user

    def get_event_author(self):
        return self.user


class Event(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        related_name="creator"
    )

    name = models.CharField(
        u'Название события',
        max_length=511
    )

    users_to_show = models.ManyToManyField(
        settings.AUTH_USER_MODEL
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'

post_save.connect(comment_up, sender=Comment, dispatch_uid="comment_up")
post_save.connect(like_up, sender=Like, dispatch_uid="like_up")

for model in BaseEvent.__subclasses__():
    post_save.connect(base_event_post_save, sender=model, dispatch_uid=model.__name__ + " event signal")
