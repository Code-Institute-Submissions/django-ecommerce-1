from django.views.generic import ListView

from .models import Product


class ProductListView(ListView):
    """List products from database"""
    model = Product
    template_name = 'products/product_list.html'
