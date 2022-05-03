import os

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tamarcado.settings.dev")

application = get_asgi_application()
