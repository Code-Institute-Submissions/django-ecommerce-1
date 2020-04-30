from django.contrib import admin

from .models import Product, Review


class ReviewInline(admin.TabularInline):
    """Tabular Inline View for Product Reviews"""
    model = Review


class ProductAdmin(admin.ModelAdmin):
    """Update view for admin panel"""
    list_display = ('title', 'brand', 'category', 'price', 'is_live')
    list_editable = ('is_live',)
    list_filter = ('is_live', 'brand', )

    inlines = [
        ReviewInline,
    ]


admin.site.register(Product, ProductAdmin)
