from django.db import models
from django.conf import settings


class OrderStatusHistory(models.Model):

    # ✅ ВАЖНО: строковая ссылка вместо импорта
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="status_history"
    )

    status = models.CharField(max_length=50)

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    note = models.TextField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Order {self.order_id} → {self.status}"