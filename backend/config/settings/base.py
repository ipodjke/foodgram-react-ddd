import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

APPS_DIR = os.path.join(BASE_DIR, './apps')
sys.path.insert(0, APPS_DIR)

SECRET_KEY = os.environ.get('SECRET_KEY')
if SECRET_KEY is None:
    raise Exception('Не найден SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'users',
    'ingredients',
    'tags',
    'recipes',
    'subscriptions',
    'favorites',
    'shopping_cart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATE_DIR = os.path.join(APPS_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

LANGUAGES = (('ru', 'Русский'), ('en', 'English'))

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SITE_ID = 1

CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = 'users.User'

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.CreateUserSerializer',
        'user_subscriptions': 'users.serializers.SubscribtionsUserSerializer',
        'user': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.AllowAny'],
        'user_detail': ['rest_framework.permissions.AllowAny'],
    },
    'HIDE_USERS': False,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'utils.paginations.PageNumberWithPageSizeControllPagination',
    'PAGE_SIZE': 20,
    'SEARCH_PARAM': 'name',
}

PATH_PARAM_NAMES = {
    'favorited': 'is_favorited',
    'shopping_cart': 'is_in_shopping_cart',
}

ERROR_MESSAGE = {
    'alredy_favorited': 'Вы уже подписаны на этот рецепт',
    'alredy_in_cart': 'Рецепт уже есть в корзине',
    'not_in_favorited': 'Вы не подписаны на этот рецепт',
    'not_in_cart': 'У Вас нет этого рецепта в корзине',
    'self_subscription': 'Вы не можете подписаться на себя',
    'self_unsubscription': 'Вы не можете отписываться от себя',
    'alredy_subscribe': 'Вы уже подписаны на этого пользователя',
    'not_subscribe': 'Вы не подписаны на этого пользователя',
    'current_password': 'Вы указали не верный пароль от своей учетной записи',
    'both_query_params': 'Не допустимый запрос, заданы is_favorited и is_in_shopping_cart,'
                         ' выберите один',
    'unique_query_params': 'Не возможно использовать фильтрацию по author и(или) tags совместно'
                           ' c is_favorited или is_in_shopping_cart'
}
