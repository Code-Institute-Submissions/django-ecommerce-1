from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Adds additional fields to Django User model"""
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=False, unique=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=100, null=True)
    post_code = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField(null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['address', 'city', 'country', 'post_code',
                       'date_of_birth']

    def __str__(self):
        return f'{self.first_name} {self.last_name[:1]}'

    def get_absolute_url(self):
        return reverse('account_profile')
