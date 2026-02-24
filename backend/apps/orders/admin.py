from django.contrib import admin
from .models import Order, OrderItem
from django.core.exceptions import ValidationError

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email',)
    inlines = [OrderItemInline]
    ordering = ('-created_at',)

def save_model(self, request, obj, form, change):
    if obj.is_paid and change:
        raise ValidationError("Paid orders cannot be modified.")
    super().save_model(request, obj, form, change)