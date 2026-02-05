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

        # 1️⃣ Проверка корзины
        cart = request.user.cart
        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        # 2️⃣ Получаем адрес из запроса
        address_id = request.data.get("address_id")
        if not address_id:
            return Response({"error": "Address is required"}, status=400)

        try:
            from apps.addresses.models import Address
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Invalid address"}, status=400)

        # 3️⃣ Создаём заказ
        order = Order.objects.create(user=request.user, address=address)

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

        # 4️⃣ очищаем корзину
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data)
 

class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = request.user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
