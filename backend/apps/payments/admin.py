from django.contrib import admin
from .models import Payment, PaymentTransaction, PaymentHistory

class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0

class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory  # теперь ссылка на Payment
    extra = 0

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'provider', 'status', 'amount', 'created_at')
    list_filter = ('provider', 'status', 'created_at')
    search_fields = ('order__id',)
    inlines = [PaymentTransactionInline, PaymentHistoryInline]

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "payment", "success", "provider_payment_id", "idempotency_key", "created_at")
    list_filter = ("success",)
