from django.urls import path
from imdb_api.views.main import frontpage, dashboard
from imdb_api.views.signup import signup
from imdb_api.views.login_view import login_view, logout_view
from django.contrib.auth import views as auth_views  # Import Django's built-in authentication views

app_name = "imdb_api"
urlpatterns = [
    path("", frontpage, name='frontpage'),
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("Dashboard/", dashboard, name='dashboard'),
    path("logout/", logout_view, name="logout"),
    
]

