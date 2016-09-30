from __future__ import unicode_literals

from django.conf import settings
from django.db import models


# Create your models here.

class Friendship(models.Model):
    """
    Илья, посмотри, как нам лучше сделать?
    Тут нас что-то несколько смущает, может быть мы не увидели более очевидного решения?
    На данный момент состояние заявки в друзья определяется так:
    accepted_first accepted_second
           0              0       (отсутствие записи - не друзья)
           1              0       (первый отправил, второй не подтвердил)
           0              1       (второй отправил, первый не ответил)
           1              1       (друзья)
    """
    id1 = models.ForeignKey(settings.AUTH_USER_MODEL)
    id2 = models.ForeignKey(settings.AUTH_USER_MODEL)

    accepted_first = models.BooleanField(
        default=False
    )
    accepted_second = models.BooleanField(
        default=False
    )
