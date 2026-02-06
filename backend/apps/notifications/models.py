from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class NotificationSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="notifications")

    order_updates = models.BooleanField(default=True)
    promotions = models.BooleanField(default=True)
    new_products = models.BooleanField(default=True)
    seasonal_offers = models.BooleanField(default=True)

    def __str__(self):
        return f"Subscriptions for {self.user}"
