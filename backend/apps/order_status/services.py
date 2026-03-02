from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.order_status.models import OrderStatusHistory
from apps.shop.models import Product


class OrderStatusService:

    ALLOWED_TRANSITIONS = {
        "pending": ["paid", "cancelled"],
        "paid": ["shipped", "refunded"],
        "shipped": ["completed"],
        "completed": [],
        "cancelled": [],
        "refunded": [],
    }

    @staticmethod
    @transaction.atomic
    def change_status(order, new_status, user=None, note=None):

        current_status = order.status

        # 🛡 idempotency protection
        if current_status == new_status:
            return order

        allowed = OrderStatusService.ALLOWED_TRANSITIONS.get(current_status, [])

        if new_status not in allowed:
            raise ValidationError(
                f"Cannot change order status from '{current_status}' to '{new_status}'"
            )

        # 🚫 нельзя делать refund если уже shipped
        if current_status == "shipped" and new_status == "refunded":
            raise ValidationError("Cannot refund shipped order")

        # 💰 Авто refund логика
        if new_status == "refunded":
            OrderStatusService._process_refund(order)

        # 📦 Возврат stock при отмене
        if new_status in ["cancelled", "refunded"]:
            OrderStatusService._restore_stock(order)

        # меняем статус
        order.status = new_status
        order.save()

        # 🧾 история статусов
        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            changed_by=user,
            note=note
        )

        return order

    # -------------------------
    # PRIVATE METHODS
    # -------------------------

    @staticmethod
    def _restore_stock(order):
        """
        Возвращаем товары на склад
        """
        for item in order.items.all():
            try:
                product = Product.objects.get(name=item.product_name)
                product.stock += item.quantity
                product.save()
            except Product.DoesNotExist:
                continue

    @staticmethod
    def _process_refund(order):
        """
        Здесь должна быть интеграция с платежным провайдером.
        Сейчас — просто помечаем как не оплаченный.
        """
        if not order.is_paid:
            raise ValidationError("Order is not paid")

        # Тут в будущем:
        # stripe.Refund.create(...)
        # paypal refund API ...
        
        order.is_paid = False
        order.payment_id = None
        order.save()