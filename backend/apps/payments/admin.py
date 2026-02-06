from django.contrib import admin
from apps.payments.models import PaymentTransaction, PaymentHistory


class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0


@admin.register(PaymentTransaction)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "provider", "status")
    list_filter = ("provider", "status")
    inlines = [PaymentHistoryInline]
