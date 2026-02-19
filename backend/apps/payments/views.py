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

from core.throttling import PaymentThrottle

from apps.orders.models import Order
from .serializers import PaymentRequestSerializer, PaymentTransactionSerializer
from .services import PaymentService
from .services import PayPalService, CardService, CryptoService


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [PaymentThrottle]


    def post(self, request):

        serializer = PaymentRequestSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]
        payment_method = serializer.validated_data["payment_method"]
        idempotency_key = serializer.validated_data["idempotency_key"]

        order = Order.objects.get(id=order_id, user=request.user)

        provider_map = {
            "paypal": PayPalService,
            "card": CardService,
            "crypto": CryptoService,
        }

        provider_service = provider_map[payment_method]

        transaction = PaymentService.process(
            order=order,
            user=request.user,
            payment_method=payment_method,
            idempotency_key=idempotency_key,
            provider_service=provider_service,
        )

        return Response(PaymentTransactionSerializer(transaction).data)


class PaymentTransactionListView(generics.ListAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.request.query_params.get("order_id")
        # фильтруем через связанный Payment
        return PaymentTransaction.objects.filter(
            payment__order__id=order_id, payment__order__user=self.request.user
        )
