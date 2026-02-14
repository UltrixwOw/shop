# apps/payments/models.py
from django.db import models
from apps.orders.models import Order
from django.conf import settings


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
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
    external_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"


class PaymentTransaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="transactions")
    idempotency_key = models.CharField(max_length=255, unique=True)
    provider_payment_id = models.CharField(max_length=255, null=True, blank=True)
    success = models.BooleanField(default=False)
    raw_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} for Payment {self.payment.id}"


class PaymentHistory(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    raw_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.payment} → {self.status}"
