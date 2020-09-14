"""
Django settings for ama project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY','m#@f(ct*4mx7gin=-9ked(@b1-1ol-%8huzsm0p_0dtit5ak2-')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_swagger',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'django_robohash',


    'authentication.apps.AuthenticationConfig',
    'books',
    'store',
    'paypal'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ama.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [BASE_DIR, os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ama.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
         'TEST': {
            'NAME': 'test ama'
        }

    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


CELERY_BROKER_URL = 'redis://{}:{}'.format(os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT'))
CELERY_RESULT_BACKEND = 'redis://{}:{}'.format(os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT'))
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 691200}
CELERY_ALWAYS_EAGER=False
TIME_ZONE = 'UTC'

REDIS_HOST = os.environ.get('REDIS_HOST'),
REDIS_PORT = os.environ.get('REDIS_PORT'),
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

# # for Heroku
# CELERY_BROKER_URL = os.environ.get('REDIS_URL')
# CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'
# CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 691200}
# CELERY_ALWAYS_EAGER=False
# TIME_ZONE = 'UTC'




# AWS Credentials
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# # Celery
# CELERY_BROKER_URL = "sqs://%s:%s@" %(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_DEFAULT_QUEUE = 'celery'
# CELERY_RESULT_BACKEND = None # Disabling the results backend
# CELERY_ALWAYS_EAGER=False
# TIME_ZONE = 'UTC'
# CELERY_TIMEZONE = 'UTC'
# BROKER_TRANSPORT_OPTIONS = {
#     'region': 'us-east-2',
#     'polling_interval': 20,
# }

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'authentication.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
django_heroku.settings(locals())

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'ama.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY', '')
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY', '')
CUSTOMER_SERVICE_EMAIL = os.environ.get('CUSTOMER_SERVICE_EMAIL', '')
EMAIL_FROM =os.environ.get('EMAIL_FROM')
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', '')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '')
EMAIL_SWITCH = os.environ.get('EMAIL_SWITCH', '')
CACHE_TIME = int(os.environ.get('CACHE_TIME', '172800'))
EMAIL_CACHE_TIME = int(os.environ.get('EMAIL_CACHE_TIME', '7200'))
ADMIN_EMAIL =os.environ.get('ADMIN_EMAIL')
