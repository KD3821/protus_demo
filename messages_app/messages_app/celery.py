import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTING_MODULE", "messages_app.settings")
app = Celery("messages_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


"""
export DJANGO_SETTINGS_MODULE=messages_app.settings
python3 -m celery -A messages_app worker --loglevel=info
python3 -m celery -A messages_app beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
"""