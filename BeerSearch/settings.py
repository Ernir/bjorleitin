"""
Django settings for BeerSearch project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG_MODE")))
TEMPLATE_DEBUG = DEBUG

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # "debug_toolbar", # I comment this in and out, sue me.
    "beer_search",
    "crispy_forms",
    "storages"
)

CRISPY_TEMPLATE_PACK = "bootstrap3"

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'BeerSearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'BeerSearch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Parse database configuration from $DATABASE_URL
DATABASES = {"default": dj_database_url.config("BEER_DB_URL")}
# Enable Connection Pooling
DATABASES["default"]["ENGINE"] = "django_postgrespool"
# Stuff from Heroku quickstart:

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config("BEER_DB_URL")


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'is'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# AWS setup

AWS_ACCESS_KEY_ID = os.environ.get("BEER_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("BEER_AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "bjorleit"
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

AWS_HEADERS = {
    "Cache-Control": "max-age=86400",  # 24 hours
}

# Media file configuration

DEFAULT_FILE_STORAGE = 'BeerSearch.s3utils.MediaRootS3BotoStorage'
MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME

# Static file configuration

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
if not DEBUG:
    STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
    STATICFILES_STORAGE = 'BeerSearch.s3utils.StaticRootS3BotoStorage'
else:
    STATIC_URL = '/static/'