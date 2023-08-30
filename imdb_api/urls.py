from django.urls import path
from imdb_api.views.main import main

app_name = "imdb_api"
urlpatterns = [
    path("",main,name="home" ),
    
]

