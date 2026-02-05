from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem
from .serializers import OrderSerializer

from apps.cart.models import CartItem


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart = request.user.cart
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        order = Order.objects.create(user=request.user)

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

        # очищаем корзину
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data)

class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = request.user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
