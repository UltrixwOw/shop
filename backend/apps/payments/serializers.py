from rest_framework import serializers
from apps.payments.models import PaymentTransaction
from apps.orders.models import Order


class PaymentTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentTransaction
        fields = "__all__"
        read_only_fields = ["amount", "status"]

    def validate(self, data):

        order = data["order"]

        if hasattr(order, "payment"):
            raise serializers.ValidationError("Payment already exists")

        return data


class PaymentRequestSerializer(serializers.Serializer):

    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=["paypal", "card", "crypto"])

    def validate(self, data):

        user = self.context["request"].user
        order_id = data["order_id"]

        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found")

        if order.total_price <= 0:
            raise serializers.ValidationError("Invalid order amount")

        # Проверяем, не оплачен ли уже заказ
        if hasattr(order, "paymenttransaction"):
            raise serializers.ValidationError("Order already paid")

        return data
