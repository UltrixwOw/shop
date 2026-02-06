from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.orders.models import Order
from .models import OrderHistory
from .serializers import OrderHistorySerializer

from rest_framework.permissions import IsAdminUser

class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        history = order.history.all().order_by('timestamp')
        serializer = OrderHistorySerializer(history, many=True)
        return Response(serializer.data)

class AdminAllOrdersHistoryView(APIView):
    permission_classes = [IsAdminUser]  # только админ

    def get(self, request):
        orders = Order.objects.all().order_by('-id')
        result = []

        for order in orders:
            history = order.history.all().order_by('timestamp')
            serializer = OrderHistorySerializer(history, many=True)
            result.append({
                "order_id": order.id,
                "user": str(order.user),
                "current_status": order.status,
                "history": serializer.data
            })

        return Response(result)