# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext as _l
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class WithContentType(models.Model):
    def get_content_type(self):
        return ContentType.objects.get_for_model(self)

    class Meta:
        abstract = True


class WithComment(models.Model):
    count_comments = models.PositiveIntegerField(
        _l(u'Число комментариев'),
        default=0
    )

    class Meta:
        abstract = True


class WithLike(models.Model):
    count_likes = models.PositiveIntegerField(
        _l(u'Число лайков'),
        default=0
    )

    class Meta:
        abstract = True


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _l(u'Лайк')
        verbose_name_plural = _l(u'Лайки')


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
        verbose_name = _l(u'Событие')
        verbose_name_plural = _l(u'События')
        abstract = True


class Album(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1
    )

    created_at = models.DateField(
        _l(u'Дата создания'),
        auto_now_add=True
    )

    name = models.CharField(
        _l(u'Название'),
        max_length=40,
        default=None
    )

    description = models.CharField(
        _l(u'Описание'),
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
        _l(u'Превью'),
        default=False
    )

    description = models.CharField(
        _l(u'Описание'),
        max_length=255,
        default=None
    )

    added_at = models.DateField(
        _l(u'Дата добавления'),
        auto_now_add=True
    )

    photo = models.FileField(
        upload_to=upload_photos,
        default=''
    )

    class Meta:
        verbose_name = _l(u'Фото')
        verbose_name_plural = _l(u'Фото')
        abstract = False

    def get_event_name(self):
        return _l(u"%s %s добавил новую фотографию в альбом %s ") % (
            self.album.user.firstname, self.album.user.lastname, self.album.name)

    def get_event_author(self):
        return self.album.user


def upload_attachments(obj, filename):
    to = "attachments" + "/" + filename
    return to


class WithAttachment(models.Model):
    attachment = models.FileField(
        upload_to=upload_attachments,
        blank=True
    )

    class Meta:
        abstract = True


class Post(BaseEvent, WithComment, WithLike, WithAttachment):
    title = models.CharField(
        _l(u'Заголовок поста'),
        max_length=255
    )

    content = models.TextField(
        _l(u'Текст поста'),
        default=None
    )

    created_at = models.DateTimeField(
        _l(u'Создан'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _l(u'Обновлен'),
        auto_now=True
    )

    class Meta:
        verbose_name = _l(u'Пост')
        verbose_name_plural = _l(u'Посты')
        abstract = False

    def get_event_name(self):
        return _l(u"Новый пост от пользователя") + " %s: %s" % (self.user, self.title)

    def get_event_author(self):
        return self.user


class Comment(BaseEvent, WithLike):
    content = models.CharField(
        _l(u'Текст комментария'),
        default=None,
        max_length=255
    )

    created_at = models.DateTimeField(
        _l(u'Создан'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _l(u'Обновлен'),
        auto_now=True
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _l(u'Комментарий')
        verbose_name_plural = _l(u'Комментарии')
        abstract = False

    def get_event_name(self):
        return "%s %s " % (self.user.firstname, self.user.lastname) + _l(u"оставил новый комментарий")

    def get_event_author(self):
        return self.user


class Meeting(BaseEvent):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participants"
    )

    description = models.TextField(
        _l(u'Описание'),
        default=_l(u'Создатель события, увы, ещё не оставил его описания')
    )

    duration = models.TimeField(
        _l(u'Длительность мероприятия'),
        default=None
    )

    when = models.DateTimeField(
        _l(u'Когда'),
        default=None
    )

    class Meta:
        verbose_name = _l(u'Встреча')
        verbose_name_plural = _l(u'Встречи')
        abstract = False

    def get_event_name(self):
        return _l(u"Вы приглашены на новую встречу: ") + self.description[100:] + "..."

    def get_event_author(self):
        return self.user


class Birthday(models.Model):
    when = models.DateTimeField(
        _l(u'Когда'),
        default=None
    )

    class Meta:
        verbose_name = _l(u'День рождения')  # translation with _ (./manage.py makemessages)
        verbose_name_plural = _l(u'Дни рождения')
        abstract = False


class Event(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        related_name="created_events"
    )

    name = models.CharField(
        _l(u'Название события'),
        max_length=511
    )

    users_to_show = models.ManyToManyField(
        settings.AUTH_USER_MODEL
    )

    created_at = models.DateTimeField(
        _l(u'Создано'),
        auto_now_add=True
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _l(u'Событие')
        verbose_name_plural = _l(u'События')
        ordering = ['created_at']




