from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .serializers import OrderStatusSerializer
from apps.orders.models import Order
from .services import OrderStatusService

class OrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]  # Только админ может менять статус

    def post(self, request, order_id):
        serializer = OrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        OrderStatusService.change_status(
            order,
            serializer.validated_data['status'],
            user=request.user,
            note=serializer.validated_data.get('note')
        )

        return Response({"success": True, "status": order.status})
