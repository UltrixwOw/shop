# shop/views.py
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from apps.common.permissions import IsAdminOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer