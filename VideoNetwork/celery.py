import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VideoNetwork.settings')
 
app = Celery('VideoNetwork')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'notify_message_not_read': {
        'task': 'chat.tasks.notify_message_not_read',
        'schedule': crontab(minute='*/1'),
    },
}
app.conf.timezone = 'Europe/Berlin'
