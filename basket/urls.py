from django.urls import path

from .views import add_to_basket, view_basket, remove_from_basket, \
    update_basket

urlpatterns = [
    path('', view_basket, name='basket'),
    path('add/<uuid:product>/', add_to_basket, name='add_to_basket'),
    path('remove/<uuid:product>/', remove_from_basket,
         name='remove_from_basket'),
    path('update/', update_basket, name='update_basket'),
]
