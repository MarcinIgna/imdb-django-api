from django.urls import path
from imdb_api.views.main import main, frontpage
from imdb_api.views.signup import signup

app_name = "imdb_api"
urlpatterns = [
    path("",main,name="main"),
    path("base/", frontpage, name='frontpage'),
    path("signup/", signup, name="signup")
    
]

