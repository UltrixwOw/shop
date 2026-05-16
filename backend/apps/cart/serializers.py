# apps/cart/serializers.py

from rest_framework import serializers

from .models import Cart, CartItem
from apps.shop.models import Product

print("🔥🔥🔥 CART SERIALIZER LOADED! 🔥🔥🔥")


class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    product_stock = serializers.IntegerField(
        source="product.stock",
        read_only=True
    )

    # FULL IMAGE
    product_image = serializers.SerializerMethodField()

    # THUMBNAIL
    product_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "price",
            "quantity",
            "product_stock",
            "product_image",
            "product_thumbnail",
        ]

    def _get_main_image(self, obj):
        image = None

        if hasattr(obj.product, "_prefetched_objects_cache"):
            images = obj.product._prefetched_objects_cache.get("images")

            if images:
                image = images[0]

        if not image:
            image = obj.product.images.first()

        return image

    def get_product_image(self, obj):
        image = self._get_main_image(obj)

        if not image:
            return None

        request = self.context.get("request")

        url = image.image.url

        if request:
            return request.build_absolute_uri(url)

        return url

    def get_product_thumbnail(self, obj):
        print("🟢 get_product_thumbnail вызван!")
        image = self._get_main_image(obj)

        if not image or not image.thumbnail:
            return self.get_product_image(obj)

        request = self.context.get("request")

        url = image.thumbnail.url

        if request:
            return request.build_absolute_uri(url)

        return url


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = ["id", "items"]


class AddToCartSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()

    quantity = serializers.IntegerField()

    def validate_product_id(self, value):

        if not Product.objects.filter(
            id=value,
            is_active=True
        ).exists():
            raise serializers.ValidationError(
                "Product not available"
            )

        return value

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero"
            )

        if value > 100:
            raise serializers.ValidationError(
                "Too many items"
            )

        return value