import os

import dj_database_url
from decouple import Csv, config
from unipath import Path
from django.contrib import admin



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


PROJECT_DIR = Path(__file__).parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'tb.activities',
    'tb.api',
    'tb.authentication',
    'tb.core',
    'tb.medications',
    'tb.messenger',
    'tb.search',
    'tb.feeds',
    'bootstrap3',
    'twilio',
    'formtools',
    'explorer',
    'django_tables2',
    'crispy_forms',
    'import_export',
    'tablib',
    'sendgrid',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',

    
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tb.urls'

WSGI_APPLICATION = 'tb.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_DIR.child('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Central'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('pt-br', 'Portuguese'),
    ('es', 'Spanish')
)

LOCALE_PATHS = (PROJECT_DIR.child('locale'), )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_ROOT = PROJECT_DIR.parent.child('staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.child('media')
MEDIA_URL = '/media/'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/app'

ALLOWED_SIGNUP_DOMAINS = ['*']

FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0o644

TAGGIT_CASE_INSENSITIVE = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'

IMPORT_EXPORT_USE_TRANSACTIONS = True


# #Celery Broker URL#
# CELERY_BROKER_URL = 'amqp://localhost'

broker_url = os.environ.get('CLOUDAMPQ_URL')
broker_pool_limit = 1
broker_heartbeat = None
broker_connection_timeout = 30
result_backend = None
event_queue_expires = 60

##########################
####API REST Framework####
##########################

REST_FRAMEWORK = {
    #Allows for SearchFilter (/?search=YourFieldAllowedInSettings...)
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    #Paginate API Results to 10 presults per page
    'PAGE_SIZE': 10,

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

##########################
##### Auth Token Test ####
##########################

# CURL RETRIVE AUTH TOKEN
# curl -H "Content-Type: application/json" -X POST -d '{"username":"stemado","password":"Fr33d0m!"}' http://127.0.0.1:8000/api-token-auth/

# CURL TEST AUTH TOKEN
# curl -X GET http://127.0.0.1:8000/api/v1/Medication/?id=1  -H 'Authorization: Token 924fb9aac518014fbb42b57b0bf4c3fc472729af'



##########################
##### Sendgrid Email #####
##########################
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 25
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False


##########################
### Twilio Credentials ###
##########################

TWILIO_ACCOUNT_SID=config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN=config('TWILIO_AUTH_TOKEN')

###############################
## Google Chrome Credentials ##
############ FOR ##############
###### Push Notfications ######
###############################

WEBPUSH_SETTINGS = {
    "GCM_ID": "86199635270",
    "GCM_KEY":"AIzaSyDUxkSvt03YgQzILmU6fZUjQO-h9Z9bWEU"
}



