from rest_framework import serializers
from apps.payments.models import PaymentTransaction

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['id', 'order', 'user', 'payment_method', 'amount', 'status', 'provider_payment_id', 'created_at']

class PaymentRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=['paypal', 'card', 'crypto'])
