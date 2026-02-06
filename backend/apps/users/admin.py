from django.contrib import admin
from apps.users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_active", "is_staff")
    search_fields = ("email",)
    list_filter = ("is_active", "is_staff")
