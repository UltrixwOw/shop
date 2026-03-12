from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.shop.models import Product
from rest_framework import status

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
    
class CartSyncView(APIView):
    """Синхронизация локальной корзины с сервером"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST /api/cart/sync/
        Body: {"items": [{"product_id": 1, "quantity": 2}, ...]}
        """
        items = request.data.get('items', [])
        
        if not isinstance(items, list):
            return Response(
                {"error": "items must be a list"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем или создаем корзину пользователя
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        results = {
            'added': [],
            'updated': [],
            'failed': []
        }
        
        # Получаем все существующие товары в корзине
        existing_items = {item.product_id: item for item in cart.items.all()}
        
        for item in items:
            product_id = item.get('product_id') or item.get('product')
            quantity = item.get('quantity', 1)
            
            if not product_id:
                results['failed'].append({
                    'product_id': None,
                    'error': 'Missing product_id'
                })
                continue
                
            try:
                if product_id in existing_items:
                    # Обновляем существующий товар
                    cart_item = existing_items[product_id]
                    cart_item.quantity = quantity
                    cart_item.save()
                    results['updated'].append({
                        'product_id': product_id,
                        'quantity': quantity
                    })
                else:
                    # Создаем новый товар
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product_id=product_id,
                        quantity=quantity
                    )
                    results['added'].append({
                        'product_id': product_id,
                        'quantity': quantity
                    })
                    
            except Exception as e:
                results['failed'].append({
                    'product_id': product_id,
                    'error': str(e)
                })
        
        # Возвращаем обновленную корзину с использованием вашего сериализатора
        cart_items = cart.items.all().select_related('product')
        serializer = CartItemSerializer(cart_items, many=True)
        
        return Response({
            'items': serializer.data,
            'sync_results': results
        }, status=status.HTTP_200_OK)