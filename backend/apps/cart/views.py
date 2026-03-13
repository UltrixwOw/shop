from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartItemSerializer
from apps.shop.models import Product


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = (
            CartItem.objects.filter(cart__user=request.user)
            .select_related("product")
            .prefetch_related("product__images")
        )

        serializer = CartItemSerializer(items, many=True, context={"request": request})

        return Response({"items": serializer.data})


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.only("id", "price", "stock").get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        if quantity > product.stock:
            return Response({"error": "Недостаточно товара на складе"}, status=400)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            item.quantity = quantity
        else:
            new_quantity = item.quantity + quantity

            if new_quantity > product.stock:
                return Response({"error": "Недостаточно товара"}, status=400)

            item.quantity = new_quantity

        item.save()

        serializer = CartItemSerializer(item, context={"request": request})

        return Response(serializer.data)


class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):

        item = CartItem.objects.filter(id=item_id, cart__user=request.user).first()

        if not item:
            return Response({"error": "Not found"}, status=404)

        item.delete()

        return Response({"status": "removed", "success": True})


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):

        quantity = int(request.data.get("quantity", 1))

        item = (
            CartItem.objects.filter(id=item_id, cart__user=request.user)
            .select_related("product")
            .first()
        )

        if not item:
            return Response({"error": "Not found"}, status=404)

        if quantity > item.product.stock:
            return Response({"error": "Недостаточно товара"}, status=400)

        item.quantity = quantity
        item.save()

        serializer = CartItemSerializer(item, context={"request": request})

        return Response(serializer.data)


class CartSyncView(APIView):
    """Синхронизация локальной корзины с сервером"""

    permission_classes = [IsAuthenticated]

    def post(self, request):

        items = request.data.get("items", [])

        if not isinstance(items, list):
            return Response(
                {"error": "items must be a list"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)

        results = {"added": [], "updated": [], "failed": []}

        existing_items = {item.product_id: item for item in cart.items.select_related("product")}

        for item in items:

            product_id = item.get("product_id") or item.get("product")
            quantity = item.get("quantity", 1)

            if not product_id:
                results["failed"].append(
                    {"product_id": None, "error": "Missing product_id"}
                )
                continue

            try:
                product = Product.objects.get(id=product_id)

                if quantity > product.stock:
                    results["failed"].append(
                        {"product_id": product_id, "error": "Not enough stock"}
                    )
                    continue

                if product_id in existing_items:

                    cart_item = existing_items[product_id]
                    cart_item.quantity = quantity
                    cart_item.save()

                    results["updated"].append(
                        {"product_id": product_id, "quantity": quantity}
                    )

                else:

                    CartItem.objects.create(
                        cart=cart, product=product, quantity=quantity
                    )

                    results["added"].append(
                        {"product_id": product_id, "quantity": quantity}
                    )

            except Product.DoesNotExist:

                results["failed"].append(
                    {"product_id": product_id, "error": "Product not found"}
                )

        cart_items = (
            CartItem.objects.filter(cart__user=request.user)
            .select_related("product")
            .prefetch_related("product__images")
            .order_by("id")
        )

        serializer = CartItemSerializer(
            cart_items, many=True, context={"request": request}
        )

        return Response({"items": serializer.data, "sync_results": results})
