from django.contrib import admin
from django.urls import path, include
from shortening_service.api import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(urls))
]
