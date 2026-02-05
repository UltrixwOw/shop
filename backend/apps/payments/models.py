from django.db import models
from django.conf import settings
from apps.orders.models import Order

class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)  # PayPal / Card / Crypto
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider_payment_id = models.CharField(max_length=100, blank=True, null=True)  # id от провайдера
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - {self.status} - {self.amount}"
