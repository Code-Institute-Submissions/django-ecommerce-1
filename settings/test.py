import os

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'placeholder-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'postgres',
    }
}
