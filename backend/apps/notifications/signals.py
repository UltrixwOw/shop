from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import NotificationSubscription

User = get_user_model()


@receiver(post_save, sender=User)
def create_notification_subscription(sender, instance, created, **kwargs):
    if created:
        NotificationSubscription.objects.create(user=instance)
