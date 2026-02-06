from django.contrib import admin
from apps.addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "city", "street", "is_default")
    list_filter = ("city", "is_default")
