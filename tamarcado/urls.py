from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", healthcheck),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("agenda.urls")),
]
