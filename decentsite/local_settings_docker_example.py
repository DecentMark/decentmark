from decentsite.settings import *

# Generate a new key with:
# from django.core.management.utils import get_random_secret_key
# get_random_secret_key()
# Source: https://github.com/django/django/blob/d46bf119799f4d319f41d890366bc8154017b432/django/core/management/utils.py#L76
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm!388n2g@k%r&y)f6)pw!3=x==qn10_(+75b-hmd8&#ghq4qg@'

# Allowed Hosts needs to be set if debug is false
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: Comment this out for production
AUTH_PASSWORD_VALIDATORS = []

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DATABASE BACKEND SETTINGS
# Docker containers should not be used for important databases.
# Change this to your production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
