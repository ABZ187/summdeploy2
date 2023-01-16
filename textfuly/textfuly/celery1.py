from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# from app.tasks import send_scheduled_mails
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'textfuly.settings')

app = Celery('textfuly')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-weekly-mail': {
        'task': 'send_scheduled_mails',
        'schedule': crontab(hour=15, minute=50),
        # 'args': (2,)
    }

}

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# celery -A textfuly.celery worker --pool=solo -l info
# celery -A textfuly beat -l INFO
