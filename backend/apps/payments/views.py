from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from apps.payments.models import Payment, PaymentTransaction
from apps.payments.serializers import (
    PaymentRequestSerializer,
    PaymentTransactionSerializer,
)
from apps.order_status.services import OrderStatusService
from .services import PayPalService, CardService, CryptoService
from .serializers import PaymentTransactionSerializer
from .models import PaymentTransaction
from rest_framework import generics, permissions


# Заглушки сервисов оплаты
class PayPalService:
    @staticmethod
    def process_payment(order):
        return {"success": True, "provider_payment_id": f"paypal-{order.id}"}

class CardService:
    @staticmethod
    def process_payment(order):
        return {"success": True, "provider_payment_id": f"card-{order.id}"}

class CryptoService:
    @staticmethod
    def process_payment(order):
        return {"success": True, "provider_payment_id": f"crypto-{order.id}"}


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentRequestSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        order = serializer.validated_data["order"]
        payment_method = serializer.validated_data["payment_method"]
        idempotency_key = serializer.validated_data["idempotency_key"]

        service_map = {
            "paypal": PayPalService,
            "card": CardService,
            "crypto": CryptoService,
        }
        service = service_map[payment_method]

        with transaction.atomic():
            # 🔐 Проверка idempotency
            payment = getattr(order, "payment", None)
            if payment:
                existing_tx = payment.transactions.filter(
                    idempotency_key=idempotency_key
                ).first()
                if existing_tx:
                    return Response(PaymentTransactionSerializer(existing_tx).data)
            else:
                payment = Payment.objects.create(
                    order=order,
                    provider=payment_method,
                    status="pending",
                    amount=order.total_price,
                )

            # Выполнение оплаты
            result = service.process_payment(order)

            # Создание транзакции
            transaction_obj = PaymentTransaction.objects.create(
                payment=payment,
                idempotency_key=idempotency_key,
                provider_payment_id=result.get("provider_payment_id"),
                success=result.get("success"),
                raw_response=result,
            )

            # Если успех — меняем статус
            if result.get("success"):
                payment.status = "paid"
                payment.save()
                OrderStatusService.change_status(
                    order,
                    "paid",
                    user=request.user,
                    note=f"Payment via {payment_method}",
                )

        return Response(PaymentTransactionSerializer(transaction_obj).data)


class PaymentTransactionListView(generics.ListAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.request.query_params.get("order_id")
        # фильтруем через связанный Payment
        return PaymentTransaction.objects.filter(
            payment__order__id=order_id, payment__order__user=self.request.user
        )
