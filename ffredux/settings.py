"""
Django settings for ffredux project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from distutils.debug import DEBUG
from pathlib import Path
from urllib.parse import urlparse
from django.core.management.utils import get_random_secret_key
import os
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR=os.path.join(BASE_DIR,'ffredux','static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.getenv("DEBUG",False) == True
DEBUG = True

# ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS","sea-turtle-app-e659n.ondigitalocean.app","127.0.0.1,localhost").split(",")
ALLOWED_HOSTS = ["sea-turtle-app-e659n.ondigitalocean.app","127.0.0.1","localhost"]

# Application definition
# test
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storages',
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

ROOT_URLCONF = 'ffredux.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
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

WSGI_APPLICATION = 'ffredux.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# if os.getenv("DATABASE_URL","") != "":
#     r = urlparse(os.environ.get("DATABASE_URL"))
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql_psycopg2",
#             "NAME": os.path.relpath(r.path,"/"),
#             "USER": r.username,
#             "PASSWORD": r.password,
#             "HOST": r.hostname,
#             "PORT": r.port,
#             "OPTIONS": {"sslmode":"require"},

#         }
#     }
# else:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "db",
        "USER": "db",
        "PASSWORD": "AVNS_ACtAEacjkbZM9SDoUXn",
        "HOST": "app-59423da4-d3ac-4d59-83fc-32b9f928e1bf-do-user-11866930-0.b.db.ondigitalocean.com",
        "PORT": "25060",
        "OPTIONS": {"sslmode":"require"},

    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR,"staticfiles")
...
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# import environ
# env = environ.Env()

AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'nwoaffl-static'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
AWS_LOCATION = 'static'
AWS_S3_REGION_NAME='us-east-1'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'ffredux/static'),]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATIC_URL = '/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'