# apps/orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from apps.addresses.models import Address
from apps.cart.models import CartItem
from .models import Order, OrderItem
from .serializers import CheckoutSerializer, OrderSerializer
from apps.order_status.services import OrderStatusService
from rest_framework.exceptions import ValidationError
from .services import OrderService

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        address_id = serializer.validated_data.get("address_id")

        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=404)

        try:
            order = OrderService.checkout(
                user=request.user,
                address=address,
                cart=getattr(request.user, "cart", None),
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        return Response(OrderSerializer(order).data)

class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = request.user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, order_id):
        new_status = request.data.get("status")

        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(id=order_id)

                OrderStatusService.change_status(
                    order,
                    new_status,
                    user=request.user,
                    note="Changed via admin API"
                )

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        return Response({"status": order.status})