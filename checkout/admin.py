from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product', )
    readonly_fields = ('price', )
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'user', 'status')
    list_display_links = ('id', 'order_date', )
    list_editable = ('status',)
    list_filter = ('status', 'order_date', )
    fieldsets = (
        (None, {'fields': ('user', 'status', )}),
        (
            'Billing Details', {
                'fields': (
                    'billing_name',
                    'billing_address',
                    'billing_city',
                    'billing_country',
                    'billing_post_code',
                )
            }
        ),
        (
            'Shipping Details', {
                'fields': (
                    'shipping_name',
                    'shipping_address',
                    'shipping_city',
                    'shipping_country',
                    'shipping_post_code',
                )
            }
        )
    )
    inlines = [
        OrderItemInline,
    ]


admin.site.register(Order, OrderAdmin)
