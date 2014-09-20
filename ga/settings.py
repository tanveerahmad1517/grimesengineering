"""
Django settings for ga project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import dj_database_url
import os

## HEROKU SPECIFIC VALUES
DATABASES = {'default': dj_database_url.config()}

# SET THE VALUE THUSLY
# heroku config:add MEMBER_PASSWORD=my-secret-password
MEMBER_PASSWORD = os.environ.get('MEMBER_PASSWORD')

# heroku config:add SECRET_KEY=my-secret-password
SECRET_KEY = os.environ.get('SECRET_KEY')

## OVERRIDE ABOVE HEROKU VALUES WITH CONSTANTS FROM local_settings.py FOR LOCAL DEVELOPMENT
try:
    from local_settings import *  # @UnusedWildImport
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# heroku config:add MEMBER_PASSWORD=my-secret-password
MEMBER_PASSWORD = os.environ.get('MEMBER_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
USE_TZ = False
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ga',
    'ga.about',
    'ga.jobs',
    'ga.services',
    'tinymce',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/templates" % (BASE_DIR),
)

ROOT_URLCONF = 'ga.urls'

WSGI_APPLICATION = 'ga.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = [
    ## DJANGO
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    
    'ga.services.context_processor',
    'ga.jobs.context_processor',
]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

#===============================================================================
# AMAZON S3 CONFIG FOR MEDIA FILES
#===============================================================================
AWS_STORAGE_BUCKET_NAME = "grimes.media"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
## heroku config:add AWS_ACCESS_KEY_ID=my-secret-password
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
## heroku config:add AWS_SECRET_ACCESS_KEY=my-secret-password
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Imagekit to use s3 backend
IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'imagekit.imagecache.NonValidatingImageCacheBackend'
IMAGEKIT_DEFAULT_FILE_STORAGE = DEFAULT_FILE_STORAGE

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
MEDIA_URL = 'http://grimes.media.s3.amazonaws.com/'

#===============================================================================
# TINYMCE
#===============================================================================
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}