from rest_framework import serializers
from .models import OrderHistory

class OrderHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.StringRelatedField()  # username вместо id

    class Meta:
        model = OrderHistory
        fields = ['status', 'changed_by', 'timestamp', 'note']
