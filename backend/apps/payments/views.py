from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PaymentTransaction
from .serializers import PaymentRequestSerializer, PaymentTransactionSerializer
from .services import PayPalService, CardService, CryptoService
from apps.orders.models import Order
from apps.order_status.services import OrderStatusService


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]
        payment_method = serializer.validated_data["payment_method"]

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        # Выбираем сервис по методу оплаты
        service = {
            "paypal": PayPalService,
            "card": CardService,
            "crypto": CryptoService,
        }[payment_method]

        result = service.process_payment(order)

        # Создаём запись о транзакции
        transaction = PaymentTransaction.objects.create(
            order=order,
            user=request.user,
            payment_method=payment_method,
            amount=order.total_price,
            provider_payment_id=result.get("provider_payment_id"),
            status="paid" if result.get("success") else "failed",
        )

        # Меняем статус заказа, если оплата прошла
        if result.get("success"):
            OrderStatusService.change_status(
                order, "paid", user=request.user, note=f"Payment via {payment_method}"
            )
            order.payment_method = payment_method
            order.save()

        response_serializer = PaymentTransactionSerializer(transaction)
        return Response(response_serializer.data)
