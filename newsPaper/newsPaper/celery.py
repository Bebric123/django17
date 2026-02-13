import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsPaper.settings')

app = Celery('newsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False
app.conf.timezone = 'Europe/Moscow' 

app.conf.beat_schedule = {
    'send-weekly-news-every-monday-8am': {
        'task': 'news.tasks.send_weekly_news',
        'schedule': crontab(
            hour=13,           # Час (0-23)
            minute=5,          # Минуты (0-59)
            day_of_week='friday'  # День недели: monday, tuesday, wednesday, thursday, friday, saturday, sunday
        ),
        'args': (),
    },
    # 'send-weekly-news-test': {
    #     'task': 'news.tasks.send_weekly_news',
    #     'schedule': crontab(minute='*/2'),
    #     'args': (),
    #     'options': {
    #         'expires': 60,
    #     }
    # },
}

app.autodiscover_tasks(['news'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')