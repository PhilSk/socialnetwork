# -*- coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager, BaseUserManager
from django.core.cache import caches

from django.db import models

# Create your models here.
from friendship.models import Friendship
from django.utils.translation import ugettext as _l
import logging

cache = caches['default']
logger = logging.getLogger(__name__)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_l(u'Email непременно должен быть указан'))

        user = self.model(
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ExtUser(AbstractBaseUser, PermissionsMixin):
    friendships = models.ManyToManyField(
        'self',
        through=Friendship,
        symmetrical=False,
        related_name="related_to+"
    )

    email = models.EmailField(
        _l(u'Электронная почта'),
        max_length=255,
        unique=True,
        db_index=True
    )

    firstname = models.CharField(
        _l(u'Имя'),
        max_length=40,
        null=True,
        blank=True
    )

    lastname = models.CharField(
        _l(u'Фамилия'),
        max_length=40,
        null=True,
        blank=True
    )

    register_date = models.DateField(
        _l(u'Дата регистрации'),
        auto_now_add=True
    )

    is_active = models.BooleanField(
        _l(u'Активен'),
        default=True
    )

    is_admin = models.BooleanField(
        _l(u'Суперпользователь'),
        default=False
    )

    def add_friendship(self, user, symm=True):
        friendship, created = Friendship.objects.get_or_create(
            sender=self,
            receiver=user
        )
        if symm:
            # avoid recursion by passing `symm=False`
            user.add_friendship(self, False)
        logger.info("Added friendship with sender %d and receiver %d" % (friendship.sender, friendship.receiver))
        return friendship

    def remove_friendship(self, user, symm=True):
        friendship = Friendship.objects.filter(
            sender=self,
            receiver=user
        )
        logger.info("Removing friendship with sender %d and receiver %d" % (friendship.sender, friendship.receiver))
        friendship.delete()
        if symm:
            # avoid recursion by passing `symm=False`
            user.remove_relationship(self, False)

    def get_friendships(self):
        return self.friendships.all()

    # Этот метод обязательно должен быть определён
    def get_full_name(self):
        return self.email

    # Подгрузка событий в ленту с использованием memcached
    def get_events_cache_key(self):
        return 'user_{}_events'.format(self.id)

    def get_events(self):
        """if we have this comment in cache get it, else get
        comments count from db and set it"""
        cache_key = self.get_events_cache_key()
        events = cache.get(cache_key)
        if events is None:
            logger.info("Cache is empty for user's events, therefore get data from db and save to the cache for the next time")
            events = self.event_set.all()
            cache.set(cache_key, events, 5)  # 5 expiry time in seconds
        return cache.get(cache_key)

    # Требуется для админки
    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        verbose_name = _l(u'Пользователь')
        verbose_name_plural = _l(u'Пользователи')
