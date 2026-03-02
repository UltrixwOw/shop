from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer
from apps.shop.models import Product

from rest_framework.permissions import IsAuthenticated

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = request.user.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        cart = request.user.cart
        product = Product.objects.get(id=product_id)

        if quantity > product.stock:
            return Response(
                {"error": "Недостаточно товара на складе"},
                status=400
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if created:
            item.quantity = quantity
        else:
            new_quantity = item.quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {"error": "Недостаточно товара"},
                    status=400
                )

            item.quantity = new_quantity

        item.save()

        return Response({"success": True})

class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        # Сначала получаем объект
        item = CartItem.objects.filter(
            id=item_id,
            cart__user=request.user  # используем cart__user как в UpdateCartItemView
        ).first()
        
        # Проверяем, существует ли объект
        if not item:
            return Response({"error": "Not found"}, status=404)
        
        # Удаляем объект
        item.delete()
        
        return Response({"status": "removed", "success": True})

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        quantity = int(request.data.get("quantity", 1))

        item = CartItem.objects.filter(
            id=item_id,
            cart__user=request.user
        ).select_related("product").first()

        if not item:
            return Response({"error": "Not found"}, status=404)

        if quantity > item.product.stock:
            return Response(
                {"error": "Недостаточно товара"},
                status=400
            )

        item.quantity = quantity
        item.save()

        return Response({"success": True})