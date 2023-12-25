"""
Django settings for billjobs project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

from .utils.path import root, BASE_DIR
from .utils.keygen import SECRET_KEY  # Secret key from generator module


SECRET_KEY = SECRET_KEY

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'develop.sqlite3',
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
INTERNAL_IPS = ['127.0.0.1']

DEBUG = True if os.environ.get("DEBUG") == "1" else False

# Application definition
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'billjobs',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

# Debug
if DEBUG == True:
    INSTALLED_APPS += ("debug_toolbar",)
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = root("static_root")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]
BILLJOBS_SLACK_TOKEN = os.environ.get('BILLJOBS_SLACK_TOKEN', False)
BILLJOBS_SLACK_CHANNEL = os.environ.get('BILLJOBS_SLACK_CHANNEL')
