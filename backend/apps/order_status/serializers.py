from rest_framework import serializers

class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ])
    note = serializers.CharField(required=False, allow_blank=True)
