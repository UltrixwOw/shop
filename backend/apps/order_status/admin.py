from django.contrib import admin
from .models import OrderStatusHistory

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'changed_by', 'note', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('order__id', 'changed_by__email')
    ordering = ('-timestamp',)
