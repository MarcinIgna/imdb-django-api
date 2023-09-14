from django.shortcuts import render, get_object_or_404
from imdb_api.models.movie_model import Movie
from django.http import Http404
from django.shortcuts import render
from imdb_api.models.movie_model import Movie
from imdb_api.models.trailer_model import TrailerVideo

# creating movie views



"""

<li><a href="{% url 'imdb:movies_by_genre' 'Action' %}" class="dropdown-item">Action</a></li>
<li><a href="{% url 'imdb:movies_by_genre' 'Romance' %}" class="dropdown-item">Romance</a></li>
<li><a href="{% url 'imdb:movies_by_genre' 'Thriller' %}" class="dropdown-item">Thriller</a></li>

"""
def movies_by_genre(request, genre):
    # Filter movies based on the selected genre
    movies = Movie.objects.filter(genre__icontains=genre)

    return render(request, 'html with movie list', {'movies': movies, 'genre': genre})
    
def all_movies(request):
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
    print('context:', context)
    print('request:', request)
    return render(request, "core/all_movies.html", context)

def new_movies(request):
    movies = Movie.objects.all()
    context = {
        'movies7': movies[24:28],
        'movies8': movies[28:32],
        'movies9': movies[32:36],
        'movies10': movies[36:40],
        'movies11': movies[40:44],
        'movies12': movies[44:48],
     }
    print('context:', context)
    print('request:', request)
    return render(request, "core/new_movies.html", context)

def movie_details(request, movie_id):
    # Get the movie with the given id
    try:
        movie = get_object_or_404(Movie, pk=movie_id)
        trailer_videos = TrailerVideo.objects.filter(movie=movie)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")
    
    return render(request, 'core/movie_details.html', {'movie': movie, 'trailers': trailer_videos})


def movie_details_with_trailers(request, movie_id):
    # Get the movie with the given id
    try:
        movie = get_object_or_404(Movie, pk=movie_id)
        trailer_videos = TrailerVideo.objects.filter(movie=movie)
    except Movie.DoesNotExist:

        raise Http404("Movie does not exist")
    
    return render(request, 'core/detail&trailer.html', {'movie': movie, 'trailers': trailer_videos})


def movie_search(request):
    query = request.GET.get('query')
    movies = []  # Change this variable name to 'movies'

    if query:
        # Perform a case-insensitive search on the Movie model
        movies = Movie.objects.filter(title__icontains=query)

    return render(request, 'core/movie_search_results.html', {'movies': movies})
