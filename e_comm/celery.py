import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_comm.settings')

app = Celery('e_comm')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()