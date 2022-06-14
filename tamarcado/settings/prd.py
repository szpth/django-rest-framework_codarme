from tamarcado.settings.base import *

ALLOWED_HOSTS = ["*"]
DEBUG = False

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY_PRD")

EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 1025)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
