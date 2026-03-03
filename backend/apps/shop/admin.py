from django.contrib import admin
from apps.shop.models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'stock', 'category')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description')
    ordering = ('-id',)
    inlines = [ProductImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

admin.site.register(ProductImage)
