from django.db import models, transaction
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from apps.addresses.models import Address
from apps.shop.models import Product
import uuid
from django.core.exceptions import ValidationError


class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        db_index=True,
    )

    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    currency = models.CharField(max_length=10, default="USD")

    payment_id = models.CharField(max_length=255, blank=True, null=True)

    is_paid = models.BooleanField(default=False)

    # ✅ SOFT DELETE
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"Order {self.uuid}"

    @property
    def can_be_paid(self):
        return self.status == "pending" and not self.is_paid

    # =========================
    # SAFE STATUS CHANGE
    # =========================

    def change_status(self, new_status, user=None, note=None):
        from apps.order_status.models import OrderStatusHistory  # 👈 импорт внутри метода

        if self.status == new_status:
            return

        allowed_transitions = {
            "pending": ["paid", "cancelled"],
            "paid": ["refunded", "shipped"],
            "shipped": ["completed"],
        }

        if new_status not in allowed_transitions.get(self.status, []):
            raise ValidationError(
                f"Нельзя изменить статус с {self.status} на {new_status}"
            )

        self.status = new_status
        self.save()

        OrderStatusHistory.objects.create(
            order=self,
            status=new_status,
            changed_by=user,
            note=note
        )

    # =========================
    # CANCEL
    # =========================

    @transaction.atomic
    def cancel(self, user=None):

        if self.status != "pending":
            raise ValidationError("Можно отменить только pending заказ")

        self._restore_stock()
        self.change_status("cancelled", user, note="Заказ отменён пользователем")

    # =========================
    # REFUND
    # =========================

    @transaction.atomic
    def refund(self, user=None):

        if self.status != "paid":
            raise ValidationError("Refund возможен только для paid заказа")

        # 🚫 если shipped — нельзя
        if self.status == "shipped":
            raise ValidationError("Нельзя вернуть отправленный заказ")

        # Здесь должна быть интеграция Stripe / PayPal
        # payment_gateway.refund(self.payment_id)

        self._restore_stock()

        self.is_paid = False
        self.save()

        self.change_status("refunded", user, note="Автоматический refund")

    # =========================
    # RESTORE STOCK
    # =========================

    def _restore_stock(self):
        for item in self.items.select_related("product"):
            if item.product:
                item.product.stock += item.quantity
                item.product.save()

    # =========================
    # SOFT DELETE
    # =========================

    def soft_delete(self):
        if self.status not in ["cancelled", "refunded", "completed"]:
            raise ValidationError("Можно удалить только завершённый заказ")

        self.is_deleted = True
        self.save()


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    # 🔥 ВАЖНО — ссылка на продукт
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items"
    )

    product_name = models.CharField(max_length=255)

    product_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]

    def get_total(self):
        return self.product_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
