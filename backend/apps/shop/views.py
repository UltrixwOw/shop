# shop/views.py
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Разные права доступа:
        - GET / list / retrieve → любой пользователь (или даже аноним)
        - POST / PUT / DELETE → только админ
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]  # любой может смотреть продукты
        return [permissions.IsAdminUser()]  # создание/редактирование → только админ
