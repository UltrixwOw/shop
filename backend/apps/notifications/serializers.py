from rest_framework import serializers
from .models import NotificationSubscription


class NotificationSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSubscription
        fields = "__all__"
        read_only_fields = ["user"]
