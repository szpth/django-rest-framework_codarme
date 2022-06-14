import os

from tamarcado.settings.base import *

ALLOWED_HOSTS = []
DEBUG = True

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY_DEV")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "0.0.0.0")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 1025)
