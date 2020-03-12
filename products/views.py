from django.views.generic import ListView, DetailView

from .models import Product


class ProductListView(ListView):
    """List products from database with pagination"""
    model = Product
    context_object_name = 'product_list'
    template_name = 'products/product_list.html'
    paginate_by = 5


class ProductDetailView(DetailView):
    """Render output for a single product which is deemed to be live"""
    queryset = Product.objects.filter(is_live=True)
    template_name = 'products/product_detail.html'
