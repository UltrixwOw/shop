from django.conf import settings
from django.db import models


class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        "shop.Product",
        related_name="reviews",
        on_delete=models.CASCADE
    )

    order_item = models.ForeignKey(
        "orders.OrderItem",
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()
    comment = models.TextField()

    is_approved = models.BooleanField(default=False)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_reviews",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.product}"