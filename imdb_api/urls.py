from django.urls import path
from imdb_api.views.main import frontpage, dashboard
from imdb_api.views.signup import signup
from imdb_api.views.login_view import login_view, logout_view
from imdb_api.views.admin_panel_view import AdminView
from imdb_api.views.movie_serializer_view import MovieView
from imdb_api.views.genre_serializer_view import GenresView
from django.contrib.auth import views as auth_views  # Import Django's built-in authentication views

app_name = "imdb_api"
urlpatterns = [
    path("", frontpage, name='frontpage'),
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("Dashboard/", dashboard, name='dashboard'),
    path("logout/", logout_view, name="logout"),
    path('movies/', AdminView.see_all_movies, name='see_all_movies'),
    
    # APIs for movies
    path("apis/movies/", MovieView.as_view(), name="apis_movies"),
    path("apis/movies/<int:pk>/", MovieView.as_view(), name="apis_movies"),
    # APIs for genres
    path("apis/genres/", GenresView.as_view(), name="genres"),
    path("apis/genres/<int:pk>/", GenresView.as_view(), name="genre"),
    
    
]

