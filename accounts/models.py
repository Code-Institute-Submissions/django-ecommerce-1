from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Adds additional fields to Django User model"""
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=100, null=True)
    post_code = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.username
