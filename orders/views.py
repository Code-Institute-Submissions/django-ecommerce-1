from django.views.generic.list import ListView
from checkout.models import Order


class OrderHistoryView(ListView):
    """Show user's orders"""
    paginate_by = 10
    template_name = 'orders/order_history.html'

    def get_queryset(self):
        user_orders = Order.objects.filter(
            user=self.request.user).order_by('-order_date', 'id')
        return user_orders
