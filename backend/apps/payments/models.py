from django.db import models
from apps.orders.models import Order


class PaymentTransaction(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    PROVIDER_CHOICES = [
        ("paypal", "PayPal"),
        ("card", "Card"),
        ("crypto", "Crypto"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")

    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for order {self.order.id}"

class PaymentHistory(models.Model):

    payment = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    raw_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.payment} -> {self.status}"
