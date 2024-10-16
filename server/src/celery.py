from celery import Celery
from celery.schedules import crontab

app = Celery(__name__)
app.config_from_object('src.config:celery_settings')
app.autodiscover_tasks(['src'])

app.conf.beat_schedule = {
    'clear_cache_every_day': {
        'task': 'src.tasks.clear_cache',
        'schedule': crontab(hour='14', minute='11'),
    }
}
app.conf.timezone = 'Europe/Moscow'
