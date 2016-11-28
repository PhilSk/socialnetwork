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
        event.creator = instance.get_event_author()
        event.object_id = instance.id
        event.content_type = instance.content_type
        event.save()
        event.users_to_show = event.creator.get_friendships()
        event.save()
