from django.shortcuts import render
from imdb_api.models.movie_model import Movie

# creating movie views

def see_all_movies(request):
    movies = Movie.objects.all()
    print('movies:', movies)
    context = {"movies": movies}
    print('context:', context)
    print('request:', request)
    return render(request, "core/moviepage.html", context)

def movie_details(request, movie_id):
    # movies_obj = Movie
    get_movie = Movie.objects.filter(id=movie_id)
    return render(request, 'movie_details.html', {'movies': get_movie})

