import os

import dj_database_url

from .base import *

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)

DATABASES = {
    'default': {}
}
DATABASES['default'].update(db_from_env)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'TRUE'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'jy-djangoapp.herokuapp.com']
