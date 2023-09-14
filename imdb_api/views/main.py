from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from imdb_api.models.movie_model import Movie


def frontpage(request):
    movies = Movie.objects.all()
    context = {
        'movies7': movies[24:28],
        'movies8': movies[28:32],
        'movies9': movies[32:36],
        'movies10': movies[36:40],
        'movies11': movies[40:44],
        'movies12': movies[44:48],
     }
    # print('context:', context)
    return render(request, 'core/frontpage.html', context)

@login_required(login_url='imdb:login')
def dashboard(request):
    user = request.user.username
    # print('user: ', user)
    movies_obj = Movie.objects.all()
    # print('movies_obj: ', movies_obj)
    # print('request:', request)
    return render(request, 'core/dashboard.html', {'user': user, 
                            'movies1': movies_obj[:4], 'movies2': movies_obj[4:8],
                            'movies3': movies_obj[8:12],'movies4': movies_obj[12:16],
                            'movies5': movies_obj[16:20],'movies6': movies_obj[20:24],})

