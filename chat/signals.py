from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message
from .tasks import new_message


@receiver(post_save, sender=Message)
def notify_new_message(sender, instance, **kwargs):
    new_message(instance)