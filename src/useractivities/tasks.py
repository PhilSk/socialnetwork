# coding=utf-8
from application.celery import app
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
import logging

cache = caches['default']

logger = logging.getLogger(__name__)

@app.task
def base_event_post_save_task(obj_id, content_type_id):
    from useractivities.models import BaseEvent
    from useractivities.models import Event
    print("Async task for events")
    content_type = ContentType.objects.get(id=content_type_id)
    print(content_type)
    if content_type is None:
        return
    print(obj_id)
    instance = content_type.model_class().objects.get(id=obj_id)
    print(instance)
    if instance is None and not isinstance(instance, BaseEvent):
        return
    event = Event()
    event.name = instance.get_event_name()
    event.user = instance.get_event_author()
    event.object_id = instance.id
    event.content_type = instance.get_content_type()
    event.save()
    event.users_to_show = event.user.get_friendships()
    users_to_show_objs = get_user_model().objects.filter(id_in=event.users_to_show)
    for user in users_to_show_objs:  # убираем ленту из кэша у всех, для кого она обновилась
        cache_key = user.get_events_cache_key()
        cache.delete(cache_key)
        logger.info("Removed %s key from cache" % cache_key)
    event.save()
