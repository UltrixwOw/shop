from rest_framework import serializers
from .models import Order, OrderItem
from apps.addresses.models import Address


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["product_name", "product_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class CheckoutSerializer(serializers.Serializer):

    address_id = serializers.IntegerField()

    def validate(self, data):

        user = self.context["request"].user

        if not user.is_verified:
            raise serializers.ValidationError("Email not verified")

        if not hasattr(user, "cart") or not user.cart.items.exists():
            raise serializers.ValidationError("Cart is empty")

        try:
            address = Address.objects.get(id=data["address_id"], user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError("Invalid address")

        return data
