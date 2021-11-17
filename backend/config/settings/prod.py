import os

from .base import *

DEBUG = int(os.environ.get('DEBUG', default=0))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '0.0.0.0').split()

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'SQL_ENGINE',
            'django.db.backends.sqlite3'
        ),
        'NAME': os.environ.get(
            'SQL_DATABASE',
            os.path.join(BASE_DIR, 'db.sqlite3')
        ),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}

STATIC_URL = '/static_django/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_django')
