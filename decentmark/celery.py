from __future__ import absolute_import
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decentsite.settings')

#app = Celery('decentmark')
app = Celery('decentmark', broker="amqp://admin:password@rabbit:5672")

app.config_from_object('django.conf:settings', namespace='CELERY')
