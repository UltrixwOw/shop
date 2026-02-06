from django.contrib import admin
from apps.shop.models import Category, Product, ProductImage


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
