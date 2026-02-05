from rest_framework import serializers
from .models import Order, OrderItem
from apps.addresses.serializers import AddressSerializer  # импортируем

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)  # добавляем адрес

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'items', 'address', 'created_at']
