from django.urls import path
from imdb_api.views.main import main, frontpage
from imdb_api.views.signup import signup
from imdb_api.views.login_view import login_view

app_name = "imdb_api"
urlpatterns = [
    path("",main,name="main"),
    path("base/", frontpage, name='frontpage'),
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    
]

