from django.urls import path

from .views import process_order

urlpatterns = [
    path('', process_order, name='checkout')
]
