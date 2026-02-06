from django.contrib import admin
from apps.notifications.models import NotificationSubscription


@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "order_updates",
        "promotions",
        "new_products",
        "seasonal_offers",
    )
