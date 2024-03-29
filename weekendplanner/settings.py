"""
Django settings for weekendplanner project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n+8o4xj0b)b=%io#c7c8!e41@u3@4tp7h#a9b$2-dsc(76d78r'

# SECURITY WARNING: don't run with debug turned on in production!
import socket
DEVELOPMENT_HOST = "ip-10-235-41-15"
PRODUCTION_HOST = "ip-10-232-38-80"
if socket.gethostname() == PRODUCTION_HOST:
    DEBUG = False
elif socket.gethostname() == DEVELOPMENT_HOST:
    DEBUG = True
else:
    DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '54.212.151.230', '.planmyny.com', '.54.203.65.146']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'requests',
    'weekendplanner.app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'weekendplanner.urls'

WSGI_APPLICATION = 'weekendplanner.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'weekendplanner',
        'USER': 'root',
        'PASSWORD': 'gator',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    '/usr/local/src/weekendplanner/templates',
)

TEMPLATE_DIRS = (
    '/usr/local/src/weekendplanner/templates',
)
