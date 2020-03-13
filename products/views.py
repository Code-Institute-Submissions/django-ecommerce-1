from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView

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


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Authorized users can add new products"""
    permission_required = 'products.add_product'
    model = Product
    fields = '__all__'
    template_name = 'products/product_create.html'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    """Authorized users can update all product fields"""
    permission_required = 'products.change_product'
    model = Product
    fields = '__all__'
    context_object_name = 'product'
    template_name = 'products/product_update.html'


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    """Authorized users can delete products"""
    permission_required = 'products.delete_product'
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('product_list')
