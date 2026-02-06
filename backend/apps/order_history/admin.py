from django.contrib import admin
from .models import OrderHistory


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "changed_by", "timestamp")
    list_filter = ("status",)
