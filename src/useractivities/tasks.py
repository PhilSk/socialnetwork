from application.celery import app
from django.contrib.contenttypes.models import ContentType


@app.task
def base_event_post_save_task(obj_id, content_type_id):
    from useractivities.models import BaseEvent
    print("Async task for events")
    from useractivities.models import Event
    content_type = ContentType.objects.filter(id=content_type_id).first()
    if content_type is None:
        return
    instance = content_type.model_class().objects.filter(id=obj_id).first()
    if instance is None and not isinstance(instance, BaseEvent):
        return
    event = Event()
    event.name = instance.get_event_name()
    event.user = instance.get_event_author()
    event.object_id = instance.id
    event.content_type = instance.get_content_type()
    event.save()
    event.users_to_show = event.user.get_friendships()
    event.save()
