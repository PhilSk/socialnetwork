# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from enum import Enum


# Create your models here.
class Statements(Enum):
    accepted = True
    declined = False


class Friendship(models.Model):
    """
    Илья, посмотри, как нам лучше сделать?
    Тут нас что-то несколько смущает, может быть мы не увидели более очевидного решения?
    На данный момент состояние заявки в друзья определяется так:
    sender_state receiver_state
        0              0       (отсутствие записи - не друзья)
        1              0       (первый отправил, второй не подтвердил)
        0              1       (второй отправил, первый не ответил)
        1              1       (друзья)
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver')

    sender_state = models.BooleanField(
        default=Statements.declined
    )
    receiver_state = models.BooleanField(
        default=Statements.declined
    )
