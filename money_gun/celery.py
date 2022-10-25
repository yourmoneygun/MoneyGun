from celery import Celery


# Create Celery
app = Celery("money_gun")
app.config_from_object("django.conf.settings", namespace="CELERY")
app.autodiscover_tasks()
