# apps/orders/services.py

from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem


class OrderService:

    @staticmethod
    @transaction.atomic
    def checkout(user, address, cart):

        if not cart:
            raise ValidationError("Cart not found")

        cart_items = cart.items.all()

        if not cart_items.exists():
            raise ValidationError("Cart is empty")

        order = Order.objects.create(
            user=user,
            address=address
        )

        total = 0

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity,
            )
            total += item.product.price * item.quantity

        order.total_price = total
        order.save()

        cart_items.delete()

        return order
