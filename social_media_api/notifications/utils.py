from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    ct = None
    obj_id = None
    if target is not None:
        ct = ContentType.objects.get_for_model(target.__class__)
        obj_id = target.pk
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=ct,
        target_object_id=obj_id
    )
