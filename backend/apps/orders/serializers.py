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
    # 🔹 делаем поле обязательным
    address_id = serializers.IntegerField(required=True)

    def validate(self, data):
        user = self.context["request"].user

        # Проверяем email
        if not user.is_verified:
            raise serializers.ValidationError("Email not verified")

        # Проверяем корзину
        if not hasattr(user, "cart") or not user.cart.items.exists():
            raise serializers.ValidationError("Cart is empty")

        # Проверяем адрес
        address_id = data.get("address_id")
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError({"address_id": "Invalid address"})

        # Можно сохранить объект адреса для CheckoutView, если нужно
        data["address"] = address

        return data
