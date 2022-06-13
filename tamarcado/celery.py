import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "tamarcado.settings.dev",
)

app = Celery(
    "tamarcado",
)

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

app.autodiscover_tasks()


@app.task
def somar(x, y):
    import time

    time.sleep(10)
    print("Somar")
    return x + y
