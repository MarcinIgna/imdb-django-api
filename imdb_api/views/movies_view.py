from django.shortcuts import render, get_object_or_404
from imdb_api.models.movie_model import Movie
from django.http import Http404
from django.shortcuts import render
from imdb_api.models.movie_model import Movie
from imdb_api.models.trailer_model import TrailerVideo

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
        # print('movie: ', movie)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")

    context = {'movie': movie}
    return render(request, 'core/movie_details.html', context)



"""        
        {% for video in trailer_videos %}
            <li>
                <a href="https://www.youtube.com/watch?v={{ video.key }}">
                    {{ video.name }}
                </a>
            </li>
        {% endfor %}
        """

def trailer_display(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
        trailer_videos = TrailerVideo.objects.filter(movie=movie)
    except Movie.DoesNotExist:
        movie = None
        trailer_videos = []

    return render(request, 'movie_detail.html', {'movie': movie, 'trailer_videos': trailer_videos})