from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfilePageView.as_view(), name='account_profile'),
]
