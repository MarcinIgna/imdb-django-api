from django.shortcuts import render, get_object_or_404
from imdb_api.models.movie_model import Movie
from django.http import Http404

# creating movie views

def all_movies(request):
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

def movie_details(request, movie_id):
    try:
        movie = Movie.objects.filter(pk=movie_id)
        print('movie: ', movie)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")

    context = {'movie': movie}
    return render(request, 'core/movie_details.html', context)

