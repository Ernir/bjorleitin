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

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "debug_toolbar",
    "beer_search",
    "beer_search_v2",
    "crispy_forms",
    "storages",
    "compressor",
    "rest_framework"
)

CRISPY_TEMPLATE_PACK = "bootstrap3"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
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

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

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

if not DEBUG:
    # Local memory cache setup
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
    CACHE_MIDDLEWARE_ALIAS = "default"
    CACHE_MIDDLEWARE_SECONDS = 60 * 5
    CACHE_MIDDLEWARE_KEY_PREFIX = ""

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Twitter setup

TWITTER_CONSUMER_KEY = os.environ.get("BEER_TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.environ.get("BEER_TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("BEER_TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("BEER_TWITTER_ACCESS_TOKEN_SECRET")

# AWS setup
AWS_ACCESS_KEY_ID = os.environ.get("BEER_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("BEER_AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "bjorleit"
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
# AWS_IS_GZIPPED = True

AWS_HEADERS = {
    "Cache-Control": "max-age=86400",  # 24 hours
}

# Media file configuration

DEFAULT_FILE_STORAGE = 'BeerSearch.s3utils.MediaRootS3BotoStorage'
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME

# Static file configuration

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_URL = '//%s.s3.amazonaws.com/compressor/' % AWS_STORAGE_BUCKET_NAME
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Compressor configuration
COMPRESS_ENABLED = bool(int(os.environ.get("COMPRESS_ENABLED")))
if COMPRESS_ENABLED:
    STATICFILES_STORAGE = 'BeerSearch.s3utils.CompressorS3BotoStorage'
    COMPRESS_OFFLINE = True
    COMPRESS_URL = STATIC_URL
    COMPRESS_STORAGE = STATICFILES_STORAGE
    COMPRESS_ROOT = STATIC_ROOT
    COMPRESS_CSS_FILTERS = [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter',
        'compressor.filters.jsmin.JSMinFilter'
    ]
else:
    STATICFILES_STORAGE = 'BeerSearch.s3utils.StaticRootS3BotoStorage'

if not COMPRESS_ENABLED:
    STATIC_URL = '/static/'
