from rest_framework import serializers
from apps.payments.models import PaymentTransaction
from apps.orders.models import Order


class PaymentRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=["paypal", "card", "crypto"])
    idempotency_key = serializers.CharField()

    def validate(self, data):
        user = self.context["request"].user
        order_id = data["order_id"]
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found")

        if order.total_price <= 0:
            raise serializers.ValidationError("Invalid order amount")

        if hasattr(order, "payment") and order.payment.status == "paid":
            raise serializers.ValidationError("Order already paid")

        data["order"] = order
        return data


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = "__all__"
        read_only_fields = ["success", "provider_payment_id", "raw_response"]
