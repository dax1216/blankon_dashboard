import os

from celery import Celery
from celery.schedules import crontab

from config.settings import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("blackon_dashboard")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    broker_url=env.str("CELERY_BROKER_URL", default="redis://127.0.0.1:6379/0"),
)
# Retrieve Bookings will trigger at midnight
# Change cron schedule to test
app.conf.beat_schedule = {
    "run-retrieve-bookings": {
        "task": "apps.dashboard.tasks.retrieve_bookings",
        "schedule": crontab(minute="0", hour="0"),
    }
}
app.autodiscover_tasks()
