from django.db.models.signals import post_save
from .tasks import base_event_post_save_task
import logging

logger = logging.getLogger(__name__)


def comment_up(sender, **kwargs):
    logger.info("Comment up signal")
    if kwargs["created"]:
        instance = kwargs["instance"]
        obj = instance.content_type.get_object_for_this_type(id=int(instance.object_id))
        obj.count_comments += 1
        obj.save()


def like_up(sender, **kwargs):
    logger.info("Like up signal")
    if kwargs["created"]:
        instance = kwargs["instance"]
        obj = instance.content_type.get_object_for_this_type(id=int(instance.object_id))
        obj.count_likes += 1
        obj.save()


def base_event_post_save(sender, **kwargs):
    logger.info("Base event post save signal")
    if kwargs["created"]:
        instance = kwargs["instance"]
        content_type = instance.get_content_type().id
        base_event_post_save_task.apply_async(countdown=3, args=[instance.id, content_type])


def init_signals():
    from useractivities.models import Comment
    from useractivities.models import Like
    from useractivities.models import BaseEvent
    post_save.connect(comment_up, sender=Comment, dispatch_uid="comment_up")
    post_save.connect(like_up, sender=Like, dispatch_uid="like_up")
    for model in BaseEvent.__subclasses__():
        post_save.connect(base_event_post_save, sender=model, dispatch_uid=model.__name__ + " event signal")
    logger.info("Signals initialization was successfully completed")
