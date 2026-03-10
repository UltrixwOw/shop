# apps/shop/views.py

from rest_framework import viewsets
from django.core.cache import cache
from django.db.models import Avg, Count, Q, Exists, OuterRef
from apps.reviews.models import Review

from .models import Product
from .serializers import ProductSerializer
from core.permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):

        user = self.request.user

        qs = Product.objects.filter(is_active=True).prefetch_related("images")

        qs = qs.annotate(
            average_rating=Avg(
                "reviews__rating",
                filter=Q(reviews__is_approved=True)
            ),
            reviews_count=Count(
                "reviews",
                filter=Q(reviews__is_approved=True)
            )
        )

        if user.is_authenticated:
            qs = qs.annotate(
                user_has_review=Exists(
                    Review.objects.filter(
                        product=OuterRef("pk"),
                        user=user
                    )
                )
            )

        return qs

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

        cache.delete("products_list")
        cache.delete("products_list_admin")