from django.db import models
from django.conf import settings
from apps.orders.models import Order

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.order.id} -> {self.status} at {self.timestamp}"
