from django.urls import path
from django.contrib.auth import views as auth_views


from imdb_api.views.main import frontpage, dashboard, admin_dashboard
from imdb_api.views.signup import signup
from imdb_api.views.login_view import login_view, logout_view
from imdb_api.views.movies_view import (
    all_movies, new_movies, movie_details_with_trailers,
    movie_details, movie_search, movies_by_genre, dash_movie_search
    )
from imdb_api.views.movie_serializer_view import MovieView
from imdb_api.views.genre_serializer_view import GenresView
from imdb_api.views.user_recommendations import user_recommendations

from imdb_api.views.admin_panel_view import AdminView
from imdb_api.views.user_panel_view import vote_for_movie, toggle_favorite, user_update_profile


app_name = "imdb"
urlpatterns = [
    path("", frontpage, name='frontpage'),

    # path for user dashboard
    path("dashboard/", dashboard, name='dashboard'),
    path('movie_search/', movie_search, name='movie_search'),
    path('dash_movie/', dash_movie_search, name='dash_movie_search'),
    path('movies-by-genre/<str:genre>/', movies_by_genre, name='movies_by_genre'),
    path('user_update_profile/', user_update_profile, name='user_update_profile'),
    
    # path for admin dashboard
        path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
        path('update_profile/<int:user_id>/', AdminView.update_user_profile, name='update_profile'),
        path('see_all_users/', AdminView.see_all_users, name='see_all_users'),
        path("delete_user/<int:user_id>/", AdminView.delete_user, name="del_user"),
        path('see_all_genres/', AdminView.see_all_genres, name='see_all_genres'),
        path('add_genre/', AdminView.add_genre, name='add_genre'),
        path("delete_genre/<int:genre_id>/", AdminView.delete_genre, name="del_genre"),
        path('see_all_movies/', AdminView.see_all_movies, name='see_all_movies'),
        path('add_movie_not_authomatic/', AdminView.add_movie_not_authomatic, name='add_movie_not_authomatic'),
    
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

    
    


