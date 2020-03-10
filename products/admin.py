from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    """Update view for admin panel"""
    list_display = ('title', 'brand', 'category', 'price', )


admin.site.register(Product)
