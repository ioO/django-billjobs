from settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q)snhw!a-rd!lfb&t1_40+)zf#&faa%$jsr0a4ez1e!+&-87o+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dev.sqlite3'),
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)
