import os

from tamarcado.settings.base import *

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY_DEV")
LOGGING = {
    **LOGGING,
    "loggers": {
        "": {
            "level": os.environ.get("DJANGO_LOG_LEVEL", "DEBUG"),
            "handlers": ["console", "file"],
        }
    },
}
