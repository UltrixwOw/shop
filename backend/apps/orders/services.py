# apps/orders/services.py

from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def broadcast_stock(product):
    """
    Отправка realtime обновления stock
    """
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "stock_updates",   # ⚠ ДОЛЖНО совпадать с consumer
        {
            "type": "stock_update",
            "product_id": product.id,
            "stock": product.stock,
        }
    )


class OrderService:

    @staticmethod
    @transaction.atomic
    def checkout(user, address, cart):

        if not cart:
            raise ValidationError("Cart not found")

        cart_items = (
            cart.items
            .select_related("product")
            .select_for_update()
        )

        if not cart_items.exists():
            raise ValidationError("Cart is empty")

        total = 0

        # Проверяем склад
        for item in cart_items:
            if item.quantity > item.product.stock:
                raise ValidationError(
                    f"{item.product.name} нет в нужном количестве"
                )

        order = Order.objects.create(
            user=user,
            address=address,
            status="pending"
        )

        # Уменьшаем склад
        for item in cart_items:

            product = item.product

            product.stock -= item.quantity
            product.save()

            # 🔥 realtime update
            broadcast_stock(product)

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_price=product.price,
                quantity=item.quantity,
            )

            total += product.price * item.quantity

        order.total_price = total
        order.save()

        cart_items.delete()

        return order