from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopping_mall.settings")

app = Celery("shopping_mall",backend="redis://127.0.0.1:6379/10")


app.config_from_object('celery_tasks.config')

app.autodiscover_tasks([
    'celery_tasks.sms',
    'celery_tasks.send_email',
])
