# apps/orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from apps.addresses.models import Address
from apps.cart.models import Cart, CartItem
from .models import Order, OrderItem
from .serializers import CheckoutSerializer, OrderSerializer
from apps.order_status.services import OrderStatusService
from rest_framework.exceptions import ValidationError
from rest_framework import status
from apps.orders.services import OrderService

# apps/orders/views.py

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        address_id = serializer.validated_data["address_id"]
        user = request.user

        # безопасно получаем адрес
        address = Address.objects.get(id=address_id, user=user)

        try:
            cart = Cart.objects.select_related("user").prefetch_related("items__product").get(user=user)
        except Cart.DoesNotExist:
            raise ValidationError("Cart not found")

        # создаём заказ через сервис
        order = OrderService.checkout(user=user, address=address, cart=cart)

        return Response({
            "order_uuid": str(order.uuid),
            "total_price": order.total_price,
            "status": order.status
        }, status=status.HTTP_201_CREATED)

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