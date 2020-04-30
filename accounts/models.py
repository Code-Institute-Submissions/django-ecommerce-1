from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """ Use email instead of username """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


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

    REQUIRED_FIELDS = ['first_name', 'last_name', 'address', 'city',
                       'country', 'post_code', 'date_of_birth']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name[:1]}'

    def get_absolute_url(self):
        return reverse('account_profile')
