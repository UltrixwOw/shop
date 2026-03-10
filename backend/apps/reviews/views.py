from rest_framework import viewsets, permissions, serializers
from django.db.models import Q

from .models import Review
from .serializers import ReviewSerializer
from apps.orders.models import OrderItem

from rest_framework.decorators import action
from rest_framework.response import Response


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_context(self):
        return {
            "request": self.request
        }

    def get_queryset(self):

        product_id = self.request.query_params.get("product")

        qs = Review.objects.filter(is_approved=True)

        if self.request.user.is_authenticated:
            qs = Review.objects.filter(
                Q(is_approved=True) | Q(user=self.request.user)
            )

        if product_id:
            qs = qs.filter(product_id=product_id)

        return qs.select_related("user")

    def perform_create(self, serializer):

        user = self.request.user
        product_id = self.request.data.get("product")

        order_item = OrderItem.objects.filter(
            order__user=user,
            product_id=product_id,
            order__status="completed"
        ).first()

        if not order_item:
            raise serializers.ValidationError(
                "You can review only purchased products"
            )

        # ❗ Проверяем существующий отзыв
        if Review.objects.filter(
            user=user,
            order_item=order_item
        ).exists():
            raise serializers.ValidationError(
                "You already left a review for this product"
            )

        serializer.save(
            user=user,
            product_id=product_id,
            order_item=order_item
        )
    
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):

        review = self.get_object()

        if review.likes.filter(id=request.user.id).exists():
            review.likes.remove(request.user)
            liked = False
        else:
            review.likes.add(request.user)
            liked = True

        return Response({
            "liked": liked,
            "likes_count": review.likes.count()
        })