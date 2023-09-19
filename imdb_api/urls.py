from django.urls import path
from django.contrib.auth import views as auth_views


from imdb_api.views.main import frontpage, dashboard
from imdb_api.views.signup import signup
from imdb_api.views.login_view import login_view, logout_view
from imdb_api.views.movies_view import all_movies, new_movies, movie_details_with_trailers, movie_details
from imdb_api.views.movie_serializer_view import MovieView
from imdb_api.views.genre_serializer_view import GenresView
from imdb_api.views.user_recommendations import user_recommendations
from imdb_api.views.user_panel_view import vote_for_movie, toggle_favorite
from imdb_api.views.movies_view import movie_search, movies_by_genre, dash_movie_search


app_name = "imdb"
urlpatterns = [
    path("", frontpage, name='frontpage'),

    # path for user dashboard
    path("dashboard/", dashboard, name='dashboard'),
    path('movie_search/', movie_search, name='movie_search'),
    path('dash_movie/', dash_movie_search, name='dash_movie_search'),
    path('movies-by-genre/<str:genre>/', movies_by_genre, name='movies_by_genre'),

    # path for Signup, Login, Logout
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('recommendations/', user_recommendations, name='user_recommendations'),
    path('vote_for_movie/<int:movie_id>/', vote_for_movie, name='vote_for_movie'),
    path('toggle_favorite/<int:movie_id>/', toggle_favorite, name='toggle_favorite'),

    # path for all movie infos.
    path('all_movies/', all_movies, name='all_movies'),
    path('new_movies', new_movies, name='new_movies'),
    path('movie_details/<int:movie_id>/', movie_details, name='movie_details'),
    path('detail&trailer/<int:movie_id>/', movie_details_with_trailers, name='detail&trailer'),
    
    # APIs for movies
    path("apis/movies/", MovieView.as_view(), name="apis_movies"),
    path("apis/movies/<int:pk>/", MovieView.as_view(), name="apis_movies"),
    # APIs for genres
    path("apis/genres/", GenresView.as_view(), name="genres"),
    path("apis/genres/<int:pk>/", GenresView.as_view(), name="genre"),
    
    
]

