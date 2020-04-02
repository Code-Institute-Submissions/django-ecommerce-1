from django.contrib import admin

from .models import Product, Review


class ReviewInline(admin.TabularInline):
    """Tabular Inline View for Product Reviews"""
    model = Review


class ProductAdmin(admin.ModelAdmin):
    """Update view for admin panel"""
    inlines = [
        ReviewInline,
    ]

    list_display = ('title', 'brand', 'category', 'price', )


admin.site.register(Product, ProductAdmin)
