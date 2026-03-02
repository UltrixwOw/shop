# apps/orders/services.py

from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class OrderService:

    @staticmethod
    @transaction.atomic
    def checkout(user, address, cart):

        if not cart:
            raise ValidationError("Cart not found")

        # 🔒 Блокируем товары на время транзакции
        cart_items = (
            cart.items
            .select_related("product")
            .select_for_update()
        )

        if not cart_items.exists():
            raise ValidationError("Cart is empty")

        total = 0

        # ==========================
        # 1️⃣ Проверяем склад
        # ==========================
        for item in cart_items:
            if item.quantity > item.product.stock:
                raise ValidationError(
                    f"{item.product.name} нет в нужном количестве"
                )

        # ==========================
        # 2️⃣ Создаём заказ
        # ==========================
        order = Order.objects.create(
            user=user,
            address=address,
            status="pending"
        )

        # ==========================
        # 3️⃣ Создаём OrderItems + уменьшаем склад
        # ==========================
        for item in cart_items:

            product = item.product

            # уменьшаем остаток
            product.stock -= item.quantity
            product.save()
            
            # 🔥 отправляем websocket событие
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                "stock",
                {
                    "type": "stock_update",
                    "product_id": product.id,
                    "stock": product.stock,
                }
            )

            # сохраняем цену на момент покупки
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_price=product.price,
                quantity=item.quantity,
            )

            total += product.price * item.quantity

        # ==========================
        # 4️⃣ Сохраняем итог
        # ==========================
        order.total_price = total
        order.save()

        # ==========================
        # 5️⃣ Очищаем корзину
        # ==========================
        cart_items.delete()

        return order