from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q, Avg
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView, FormView, View
from django.shortcuts import get_object_or_404

from .models import Product, Review
from .forms import ReviewForm


class ProductListView(ListView):
    """List products from database with pagination"""
    model = Product
    context_object_name = 'product_list'
    # to avoid inconsistent pagination results order by id
    queryset = Product.objects.get_queryset().annotate(
        rating=Avg('reviews__rating')).order_by('id')
    template_name = 'products/product_list.html'
    paginate_by = 8


class ProductDetail(View):
    """Specify which view to be used dependent on request type"""

    def get(self, request, *args, **kwargs):
        view = ProductDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProductReview.as_view()
        return view(request, *args, **kwargs)


class ProductDetailView(DetailView):
    """Render output for a single product and enable review capture"""
    queryset = Product.objects.filter(is_live=True)
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # make sure the user is logged in first
        if self.request.user.is_authenticated:
            # check to see if user has already posted review for product
            user_has_reviewed = Review.objects.filter(
                product=self.object).filter(user=self.request.user)
            # if no object was returned then user has not submitted a review
            if not user_has_reviewed:
                context['display_form'] = True

        # passthrough form for rendering in template
        context['form'] = ReviewForm()

        # get average review rating and pass through to template
        product_rating = Review.objects.filter(
            product=self.object).aggregate(Avg('rating'))

        context['product_rating'] = product_rating['rating__avg']
        return context


class ProductReview(FormView):
    """Displayed on product detail, used to add reviews"""
    template_name = 'products/product_detail.html'
    form_class = ReviewForm
    model = Review

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.form_class(request.POST)

        # store the product id passed through the url(defined as pk in urls.py)
        self.pk = kwargs.get('pk')

        if form.is_valid():
            # foreign key objects not yet added, prevent saving and add them
            review = form.save(commit=False)
            review.product = get_object_or_404(Product, pk=self.pk)
            review.user = self.request.user
            review.save()
        else:
            return self.form_invalid(form)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


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
    queryset = Product.objects.get_queryset().annotate(
        rating=Avg('reviews__rating')).order_by('id')
    # to avoid inconsistent pagination results order by id
    template_name = 'products/product_search_results.html'
    paginate_by = 8

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
