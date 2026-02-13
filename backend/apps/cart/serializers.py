from rest_framework import serializers
from .models import Cart, CartItem
from apps.shop.models import Product


class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "price", "quantity"]


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items"]


class AddToCartSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_product_id(self, value):

        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Product not available")

        return value

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")

        if value > 100:
            raise serializers.ValidationError("Too many items")

        return value
