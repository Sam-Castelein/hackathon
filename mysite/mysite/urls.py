from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("billscan/", include("billscan.urls")),
    path("admin/", admin.site.urls),
]
