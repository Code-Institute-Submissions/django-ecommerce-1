from django.contrib import admin

from .models import Basket, BasketItem
# Register your models here.
admin.site.register(Basket)
admin.site.register(BasketItem)
