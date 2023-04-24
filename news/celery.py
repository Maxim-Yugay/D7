import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'weekly_post': {
        'task': 'board.tasks.my_job',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
    'print_every_5_seconds': {
        'task': 'board.tasks.printer',
        'schedule': 5,
        'args': (5,),
    },
}



app.autodiscover_tasks()