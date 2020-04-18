from django.urls import path

from .views import add_to_basket, view_basket

urlpatterns = [
    path('', view_basket, name='basket'),
    path('add/<uuid:product_id>/', add_to_basket, name='add_to_basket'),
]
