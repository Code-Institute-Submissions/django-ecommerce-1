from django.views.generic import TemplateView
from django.db.models import Count, Avg

from products.models import Product


class HomePageView(TemplateView):
    """Show most popular and newest products to end-user"""
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # get top 5 sellers
        context['most_popular'] = Product.objects.annotate(
            items_sold=Count('orderitem'),
            rating=Avg('reviews__rating')).order_by('-items_sold')[:5]
        # get the last 5 products added
        context['new_products'] = Product.objects.annotate(
            rating=Avg('reviews__rating')).order_by('-id')[:5]
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'
