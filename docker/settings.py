# Django settings for layerindex project.
#
# Based on settings.py from the Django project template
# Copyright (c) Django Software Foundation and individual contributors.
#
# SPDX-License-Identifier: MIT

import os

DEBUG = os.getenv('DEBUG', False)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'layersdb',
        'USER': os.getenv('DATABASE_USER', 'root'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'testingpw'),
        'HOST': os.getenv('DATABASE_HOST', 'layersdb'),
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Etc/UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Avoid specific paths
BASE_DIR = os.path.dirname(__file__)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/usr/share/nginx/html/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('SECRET_KEY', '')

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'layerindex.middleware.NonAtomicRevisionMiddleware',
)

# We allow CORS calls from everybody
CORS_ORIGIN_ALLOW_ALL = True
# for the API pages
CORS_URLS_REGEX = r'.*/api/.*';


# Clickjacking protection
X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + "/templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'layerindex.context_processors.layerindex_context',
            ],
        },
    },
]

# New in Django 3.2
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'layerindex',
    'django_registration',
    'reversion',
    'reversion_compare',
    'captcha',
    'axes',
    'rest_framework',
    'corsheaders',
)

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'password_validation.ComplexityValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'layerindex.restperm.ReadOnlyPermission',
    ),
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%m:%S+0000',
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Set bootstrap alert CSS styles for each message level
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.SUCCESS: 'alert-success',
    messages.INFO: 'alert-info',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Registration settings
ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = os.getenv('EMAIL_HOST', 'layers.test')
EMAIL_PORT = os.getenv('EMAIL_PORT', '25')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', False)
EMAIL_HOST_USER = os.getenv('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'noreply@' + os.getenv('HOSTNAME', 'layers.test')
LOGIN_REDIRECT_URL = '/layerindex'

# Full path to directory where layers should be fetched into by the update script
LAYER_FETCH_DIR = "/opt/workdir"

# Base temporary directory in which to create a directory in which to run BitBake
TEMP_BASE_DIR = "/tmp"

# Fetch URL of the BitBake repository for the update script
BITBAKE_REPO_URL = "git://git.openembedded.org/bitbake"

# Path within the BITBAKE_REPO_URL, usually empty
BITBAKE_PATH = ""

# Core layer to be used by the update script for basic BitBake configuration
CORE_LAYER_NAME = "openembedded-core"

# Update records older than this number of days will be deleted every update
UPDATE_PURGE_DAYS = 30

# Remove layer dependencies that are not specified in conf/layer.conf
REMOVE_LAYER_DEPENDENCIES = False

# Always use https:// for review URLs in emails (since it may be redirected to
# the login page)
FORCE_REVIEW_HTTPS = True

# False to allow accounts without security questions to reset their password
SECURITY_QUESTIONS_REQUIRED = True

# Settings for layer submission feature
SUBMIT_EMAIL_FROM = 'noreply@' + os.getenv('HOSTNAME', 'layers.test')
SUBMIT_EMAIL_SUBJECT = 'OE Layerindex layer submission'

# Send email to maintainer(s) when their layer is published
SEND_PUBLISH_EMAIL = True

# RabbitMQ settings
RABBIT_BROKER = 'amqp://' + os.getenv('RABBITMQ_DEFAULT_USER', 'guest') + ':' + os.getenv('RABBITMQ_DEFAULT_PASS', 'guest') + '@layersrabbit:5672/'
RABBIT_BACKEND = 'rpc://layersrabbit/'

# Used for fetching repo
PARALLEL_JOBS = "4"

# Install flite & sox and set these to enable audio for CAPTCHA challenges (for accessibility)
#CAPTCHA_FLITE_PATH = "/usr/bin/flite"
#CAPTCHA_SOX_PATH = "/usr/bin/sox"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
AXES_CACHE = "axes_cache"
AXES_LOCKOUT_TEMPLATE = "registration/account_lockout.html"
AXES_FAILURE_LIMIT = 4
AXES_COOLOFF_TIME = 1

# Full path to directory to store logs for dynamically executed tasks
TASK_LOG_DIR = "/opt/layerindex-task-logs"

# Full path to directory where rrs tools stores logs
TOOLS_LOG_DIR = ""

USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = [os.getenv('HOSTNAME', 'layers.test')]
CSRF_TRUSTED_ORIGINS = ['https://' + os.getenv('HOSTNAME', 'layers.test')]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

