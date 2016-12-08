# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save


# Create your models here.
from useractivities.signals import like_up, comment_up


class WithContentType(models.Model):
    def get_content_type(self):
        return ContentType.objects.get_for_model(self)

    class Meta:
        abstract = True


class WithComment(models.Model):
    count_comments = models.PositiveIntegerField(
        u'Число комментариев',
        default=0
    )

    class Meta:
        abstract = True


class WithLike(models.Model):
    count_likes = models.PositiveIntegerField(
        u'Число лайков',
        default=0
    )

    class Meta:
        abstract = True


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


class BaseEvent(WithContentType, models.Model):
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
        return "%s %s оставил новый комментарий" % (self.user.firstname, self.user.lastname)

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
        return "Вы приглашены на новую встречу: " + self.description[100:] + "..."

    def get_event_author(self):
        return self.user


class Birthday(models.Model):
    when = models.DateTimeField(
        u'Когда',
        default=None
    )

    class Meta:
        verbose_name = u'День рождения'
        verbose_name_plural = u'Дни рождения'
        abstract = False


class Event(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        related_name="created_events"
    )

    name = models.CharField(
        u'Название события',
        max_length=511
    )

    users_to_show = models.ManyToManyField(
        settings.AUTH_USER_MODEL
    )

    created_at = models.DateTimeField(
        u'Создано',
        auto_now_add=True
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'
        ordering = ['created_at']

post_save.connect(comment_up, sender=Comment, dispatch_uid="comment_up")
post_save.connect(like_up, sender=Like, dispatch_uid="like_up")
