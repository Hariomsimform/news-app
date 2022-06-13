from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsproject.settings')
app = Celery('newsproject')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update-every-60-min': {
        'task': 'myapp.tasks.task_mail',
        'schedule': 60*60.0
    }
}
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')