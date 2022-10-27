from celery import Celery


# Create Celery
app = Celery("money_gun")
app.config_from_object("django.conf.settings", namespace="CELERY")
app.conf.timezone = 'Europe/Kyiv'
app.conf.enable_utc = True
app.autodiscover_tasks()
