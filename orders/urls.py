from django.urls import path

from .views import OrderHistoryView

urlpatterns = [
    path('history/', OrderHistoryView.as_view(), name='order_history')
]
