from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from imdb_api.forms.search_form import MovieSearchForm
from imdb_api.models.genre_model import Genre
from imdb_api.models.user_favorite_model import UserFavorite
from imdb_api.models.movie_model import Movie
from imdb_api.models.trailer_model import TrailerVideo
from imdb_api.models.movie_model import Movie

def genre_list(request):
    """
    This view displays a list of genres.
    """
    genres = Genre.objects.all()
    print(genres)
    return render(request, 'core/base_navbar.html', {'genres': genres})

def genre_movies(request, genre_id):
    """
    This view displays a list of movies with a specific genre.
    """
    genre1 = Genre.objects.all()
    genre = Genre.objects.get(id=genre_id)
    movies = Movie.objects.filter(genres=genre)
    return render(request, 'core/genre_movies.html', {'genres':genre1,'genre': genre, 'movies': movies})
    
def base_genre_movies(request, genre_id):
    """
    This view displays a list of movies with a specific genre.
    """
    genre1 = Genre.objects.all()
    genre = Genre.objects.get(id=genre_id)
    movies = Movie.objects.filter(genres=genre)
    return render(request, 'core/base_genre_movies.html', {'genres':genre1,'genre': genre, 'movies': movies})

def all_movies(request):
    """
    This view displays a list of all movies used in carusele.
    """
    # All movies
    movies = Movie.objects.all()
    context = {
        'movies1': movies[:4],
        'movies2': movies[4:8],
        'movies3': movies[8:12],
        'movies4': movies[12:16],
        'movies5': movies[16:20],
        'movies6': movies[20:24],
     }
    return render(request, "core/all_movies.html", context)

def new_movies(request):
    """
    This view displays a list of new movies used in carusele.
    """
    movies = Movie.objects.all()
    context = {
        'movies7': movies[24:28],
        'movies8': movies[28:32],
        'movies9': movies[32:36],
        'movies10': movies[36:40],
        'movies11': movies[40:44],
        'movies12': movies[44:48],
     }

    return render(request, "core/new_movies.html", context)

def movie_details(request, movie_id):
    """
    This view displays the details of a movie.
    """

    try:
        genre = Genre.objects.all()
        movie = get_object_or_404(Movie, pk=movie_id)
        trailer_videos = TrailerVideo.objects.filter(movie=movie)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")
    
    return render(request, 'core/movie_details.html', {'genres': genre,'movie': movie, 'trailers': trailer_videos})


def movie_details_with_trailers(request, movie_id):
    """
    This view displays the details of a movie with trailers.
    """
    try:
        genre = Genre.objects.all()
        movie = get_object_or_404(Movie, pk=movie_id)
        trailer_videos = TrailerVideo.objects.filter(movie=movie)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")

    is_favorite = False  # Initialize as False by default

    if request.user.is_authenticated:
        # Check if the movie is in the user's favorites
        if UserFavorite.objects.filter(user=request.user, movie=movie).exists():
            is_favorite = True

    return render(request, 'core/detail&trailer.html', {'genres':genre,'movie': movie, 'trailers': trailer_videos, 'is_favorite': is_favorite})


def movie_search(request):
    """
    This view is used to search for movies.
    """
    genre = Genre.objects.all()
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            # query the database for movies that match the search term
            movies = Movie.objects.filter(title__icontains=search_term)
            return render(request, 'core/movie_search.html', {'genres': genre,'movies': movies})
    form = MovieSearchForm()
    return render(request, 'core/movie_search.html', {'genres': genre,'form': form})

def dash_movie_search(request):
    """
    This view is used to search for movies.
    """
    genre = Genre.objects.all()
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            # query the database for movies that match the search term
            movies = Movie.objects.filter(title__icontains=search_term)
            return render(request, 'core/dash_movie_search.html', {'genres': genre,'movies': movies})
    form = MovieSearchForm()
    return render(request, 'core/dash_movie_search.html', {'genres': genre, 'form': form})

