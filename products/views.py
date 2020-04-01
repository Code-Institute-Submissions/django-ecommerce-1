from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from .models import Product


class ProductListView(ListView):
    """List products from database with pagination"""
    model = Product
    context_object_name = 'product_list'
    # to avoid inconsistent pagination results order by id
    queryset = Product.objects.get_queryset().order_by('id')
    template_name = 'products/product_list.html'
    paginate_by = 6


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


class ProductSearchResultsView(ListView):
    """Return products that match search query"""
    model = Product
    context_object_name = 'search_results'
    # to avoid inconsistent pagination results order by id
    template_name = 'products/product_search_results.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Filter for search terms"""
        queryset = super().get_queryset()

        keywords = self.request.GET.get('keywords')
        if keywords:
            # filter data for anything that contains the kws
            # use the django Q object to create equivalent of SQL 'OR' query
            return queryset.filter(
                Q(title__icontains=keywords) |
                Q(brand__icontains=keywords) |
                Q(category__icontains=keywords) |
                Q(description__icontains=keywords)
            ).order_by('id')
        else:
            return ''

    def get_context_data(self, *, object_list=None, **kwargs):
        """Pass through the search terms to autopopulate search box"""
        context = super().get_context_data(**kwargs)
        # store search term in results to populate template search box
        context['search_keywords'] = self.request.GET.get('keywords')
        return context
