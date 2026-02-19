from django.db import transaction
from apps.orders.models import Order
from apps.payments.models import Payment, PaymentTransaction, PaymentHistory
from apps.order_status.services import OrderStatusService
from rest_framework.exceptions import ValidationError


class PaymentService:

    @staticmethod
    @transaction.atomic
    def process(order, user, payment_method, idempotency_key, provider_service):

        # 🔐 idempotency защита
        existing = PaymentTransaction.objects.select_for_update().filter(
            idempotency_key=idempotency_key
        ).first()

        if existing:
            return existing

        # 🔒 защита от повторной оплаты
        if hasattr(order, "payment") and order.payment.status == "paid":
            raise ValidationError("Order already paid")

        # создаём или получаем Payment
        payment, _ = Payment.objects.get_or_create(
            order=order,
            defaults={
                "provider": payment_method,
                "amount": order.total_price,
                "status": "pending",
            },
        )

        # вызываем провайдера
        result = provider_service.process_payment(order)

        # создаём транзакцию
        transaction_obj = PaymentTransaction.objects.create(
            payment=payment,
            idempotency_key=idempotency_key,
            provider_payment_id=result.get("provider_payment_id"),
            success=result.get("success"),
            raw_response=result,
        )

        # обновляем статус
        if result.get("success"):
            payment.status = "paid"
            payment.external_id = result.get("provider_payment_id")
            payment.save()

            OrderStatusService.change_status(
                order,
                "paid",
                user=user,
                note=f"Payment via {payment_method}"
            )

        else:
            payment.status = "failed"
            payment.save()

        # пишем историю
        PaymentHistory.objects.create(
            payment=payment,
            status=payment.status,
            changed_by=user,
            raw_response=result
        )

        return transaction_obj

class PayPalService:
    @staticmethod
    def process_payment(order):
        # симуляция успешной оплаты
        return {"success": True, "provider_payment_id": f"PAYPAL-{order.id}"}

class CardService:
    @staticmethod
    def process_payment(order):
        return {"success": True, "provider_payment_id": f"CARD-{order.id}"}

class CryptoService:
    @staticmethod
    def process_payment(order):
        return {"success": True, "provider_payment_id": f"CRYPTO-{order.id}"}
