from rest_framework import serializers
from .models import Order, OrderItem
from apps.addresses.models import Address


class OrderItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField(source="product.id", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "product_id",
            "product_name",
            "product_price",
            "quantity"
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

import logging
logger = logging.getLogger(__name__)

class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField(required=True)

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        logger.error("🧪 SERIALIZER START")
        logger.error(f"User: {user}")
        logger.error(f"is_verified: {getattr(user, 'is_verified', 'NO FIELD')}")
        logger.error(f"Data: {data}")

        # ✅ EMAIL CHECK
        try:
            if not user.is_verified:
                logger.error("💥 EMAIL NOT VERIFIED")
                raise serializers.ValidationError("Email not verified")
            logger.error("✅ EMAIL OK")
        except Exception as e:
            logger.error(f"💥 EMAIL CHECK ERROR: {e}")
            raise

        # ✅ CART CHECK
        try:
            has_cart = hasattr(user, "cart")
            logger.error(f"Has cart: {has_cart}")

            if not has_cart:
                raise serializers.ValidationError("Cart missing")

            items_exist = user.cart.items.exists()
            logger.error(f"Cart items exist: {items_exist}")

            if not items_exist:
                raise serializers.ValidationError("Cart is empty")

            logger.error("✅ CART OK")
        except Exception as e:
            logger.error(f"💥 CART CHECK ERROR: {e}")
            raise

        # ✅ ADDRESS CHECK
        address_id = data.get("address_id")
        try:
            logger.error(f"Looking for address_id={address_id}")
            address = Address.objects.get(id=address_id, user=user)
            logger.error(f"✅ ADDRESS OK: {address.id}")
        except Address.DoesNotExist:
            logger.error("💥 ADDRESS NOT FOUND")
            raise serializers.ValidationError({"address_id": "Invalid address"})
        except Exception as e:
            logger.error(f"💥 ADDRESS ERROR: {e}")
            raise

        data["address"] = address

        logger.error("🧪 SERIALIZER END OK")

        return data