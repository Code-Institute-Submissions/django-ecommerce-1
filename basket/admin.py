from django.contrib import admin

from .models import Basket, BasketItem


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0


class BasketAdmin(admin.ModelAdmin):
    inlines = [
        BasketItemInline,
    ]


admin.site.register(Basket, BasketAdmin)
