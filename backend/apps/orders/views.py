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

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        address_id = serializer.validated_data.get("address_id")
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=404)

        cart = getattr(request.user, "cart", None)
        if not cart:
            return Response({"error": "Cart not found"}, status=404)

        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total = 0
        with transaction.atomic():
            order = Order.objects.create(user=request.user, address=address)

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity,
                )
                total += item.product.price * item.quantity

            order.total_price = total
            order.save()

            cart_items.delete()

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
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        try:
            OrderStatusService.change_status(
                order,
                new_status,
                user=request.user,
                note=f"Changed via admin API"
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        return Response({"status": order.status})
