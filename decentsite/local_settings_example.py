from decentsite.settings import *

# Generate a new key with:
# from django.core.management.utils import get_random_secret_key
# get_random_secret_key()
# Source: https://github.com/django/django/blob/d46bf119799f4d319f41d890366bc8154017b432/django/core/management/utils.py#L76
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm!388n2g@k%r&y)f6)pw!3=x==qn10_(+75b-hmd8&#ghq4qg@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: Comment this out for production
AUTH_PASSWORD_VALIDATORS = []


# EMAIL SETTINGS
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'decentmarkapp@gmail.com'
EMAIL_HOST_PASSWORD = 'decent123456'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'no-reply <decentmarkapp@gmail.com>'

ADMINS = (
    ('You', 'decentmarkapp@gmail.com'),
)

MANAGERS = ADMINS
