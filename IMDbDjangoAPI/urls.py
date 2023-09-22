from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

#project urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("imdb_api.urls", namespace="imdb")),
    
        #swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),


]
