from django.db.models.signals import post_save


def comment_up(sender, **kwargs):
    if kwargs["created"]:
        instance = kwargs["instance"]
        obj = instance.content_type.get_object_for_this_type(id=int(instance.object_id))
        obj.count_comments += 1
        obj.save()


def like_up(sender, **kwargs):
    if kwargs["created"]:
        instance = kwargs["instance"]
        obj = instance.content_type.get_object_for_this_type(id=int(instance.object_id))
        obj.count_likes += 1
        obj.save()


def base_event_post_save(sender, **kwargs):
    if kwargs["created"]:
        instance = kwargs["instance"]
        from useractivities.models import Event
        event = Event()
        event.name = instance.get_event_name()
        event.user = instance.get_event_author()
        event.object_id = instance.id
        event.content_type = instance.get_content_type()
        event.save()
        event.users_to_show = event.user.get_friendships()
        event.save()


def init_signals():
    from useractivities.models import BaseEvent
    for model in BaseEvent.__subclasses__():
        post_save.connect(base_event_post_save, sender=model, dispatch_uid=model.__name__ + " event signal")
