from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("imdb_api.urls", namespace="imdb")),
    path("", include("imdb_api.urls", namespace="imdb"))
]
