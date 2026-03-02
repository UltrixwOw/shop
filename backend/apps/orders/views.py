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
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404

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
            cart = (
                Cart.objects.select_related("user")
                .prefetch_related("items__product")
                .get(user=user)
            )
        except Cart.DoesNotExist:
            raise ValidationError("Cart not found")

        # создаём заказ через сервис
        order = OrderService.checkout(user=user, address=address, cart=cart)

        return Response(
            {
                "order_uuid": str(order.uuid),
                "total_price": order.total_price,
                "status": order.status,
            },
            status=status.HTTP_201_CREATED,
        )


class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = request.user.orders.filter(is_deleted=False)
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
                    order, new_status, user=request.user, note="Changed via admin API"
                )

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        return Response({"status": order.status})


class OrderDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user,
            is_deleted=False
        )


class OrderByUUIDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        try:
            order = Order.objects.prefetch_related("items").get(
                uuid=uuid, user=request.user
            )
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        serializer = OrderSerializer(order)
        return Response(serializer.data)

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):

        order = get_object_or_404(
            Order,
            uuid=uuid,
            user=request.user,
            is_deleted=False
        )

        try:
            if order.status == 'pending':
                order.cancel()

            elif order.status == 'paid':
                order.refund()

            else:
                return Response(
                    {"error": "Заказ нельзя отменить"},
                    status=400
                )

        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response({"status": order.status})
    
class DeleteOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, uuid):

        order = get_object_or_404(
            Order,
            uuid=uuid,
            user=request.user,
            is_deleted=False
        )

        try:
            order.soft_delete()
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"deleted": True})