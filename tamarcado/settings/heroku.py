import django_on_heroku

from tamarcado.settings.base import *

django_on_heroku.settings(locals())
DEBUG = True
