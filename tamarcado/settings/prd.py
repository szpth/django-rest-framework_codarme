import os

from tamarcado.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY_PRD")
