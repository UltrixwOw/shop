# shop/views.py
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from core.permissions import IsAdminOrReadOnly
from django.core.cache import cache


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):

        cache_key = "products_list"

        products = cache.get(cache_key)

        if not products:
            # обычные пользователи видят только активные
            if self.request.user.is_staff:
                products = Product.objects.all()
                cache.delete("products_list")
                return products
            
            products = Product.objects.filter(is_active=True)
            cache.set(cache_key, products, timeout=300)  # 5 минут

        return products

    def get_queryset(self):

        cache_key = "products_list"

        products = cache.get(cache_key)

        if not products:
            products = Product.objects.filter(is_active=True)
            cache.set(cache_key, products, timeout=300)  # 5 минут

        return products


    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        cache.delete("products_list")
