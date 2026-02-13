from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from apps.order_status.services import OrderStatusService

from .models import Order, OrderItem
from .serializers import OrderSerializer

from apps.cart.models import CartItem

from .serializers import CheckoutSerializer
from apps.addresses.models import Address



class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CheckoutSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        address = Address.objects.get(
            id=serializer.validated_data["address_id"],
            user=request.user
        )

        cart = request.user.cart
        cart_items = cart.items.all()

        order = Order.objects.create(
            user=request.user,
            address=address
        )

        total = 0

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity
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
                user=request.user
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response({"status": order.status})