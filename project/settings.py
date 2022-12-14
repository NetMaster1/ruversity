"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hwpix$6%l_k50ftoph2^7c7fdi(5i53#p-=*#0v0xrq0f74rfe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.ruversity.com', 'ruversity.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'app_accounts',
    'app_cart',
    'app_content',
    'app_mycourses',
    'app_ratings',
    'app_reviews',
    'app_workshop',
    #'paypal.standard.ipn',
    'app_contacts',
    'storages',
    'background_task',
    'app_tutorial',
    'app_service',

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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE':   'django.db.backends.postgresql',
            'NAME': 'ruversity',
            'USER': 'postgres',
            'PASSWORD': 'ylhio65v',
            'HOST': 'localhost',
            'PORT': '5432'
    }
}

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'project/static')
]

# Media Folder Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

BACKGROUND_TASK_RUN_ASYNC = True
# CDN API settings
CDN_TIMEOUT_SECONDS = 120
CDN_FILE_UPLOAD_TIMEOUT_SECONDS = 600
#CDN_API_TOKEN = '038d0b32566d9621800255a62aea35f3eba45652' # ADAPT: replace with actual token.
CDN_API_TOKEN = 'eb91eb0d6ab5f151979155025bf124a8740ce4a8'
CDN_JWT_URL = 'https://api.cdnnow.ru/api/v3/upload/bef2861b-5668-4997-9f8c-6d6e85ad3f90/generate-jwt/video_source'
CDN_RECEIVE_UPLOAD_LINK_URL = 'https://api.cdnnow.ru/api/v3/upload/bef2861b-5668-4997-9f8c-6d6e85ad3f90/link'
CDN_VIDEO_INFO_URL = 'https://api.cdnnow.ru/api/v3/vod/projects/bef2861b-5668-4997-9f8c-6d6e85ad3f90/videos/{}'
CDN_REQUESTS_COMMON_PARAMS = {'timeout': CDN_TIMEOUT_SECONDS,
                              'headers': {"X-AUTH-TOKEN": CDN_API_TOKEN}}

FILE_UPLOAD_HANDLERS = ["django.core.files.uploadhandler.TemporaryFileUploadHandler"]


PAYPAL_RECEIVER_EMAIL = '79200711112@yandex.ru'
PAYPAL_TEST = True

#Email Settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_POSRT = 587
EMAIL_HOST_USER = 'ruversity@gmail.com'
EMAIL_HOST_PASSWORD = 'Ylhio65v_01'
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_POSRT = 537
# EMAIL_HOST_USER = '79200711112@yandex.ru'
# EMAIL_HOST_PASSWORD = 'RsK-ydU-3Ar-iYX'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
