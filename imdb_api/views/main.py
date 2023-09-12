from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from imdb_api.models.movie_model import Movie


def frontpage(request):
    return render(request, 'core/frontpage.html')

@login_required(login_url='imdb:login')
def dashboard(request):
    user = request.user.username
    # print('user: ', user)
    movies_obj = Movie.objects.all()
    # print('movies_obj: ', movies_obj)
    # print('request:', request)
    return render(request, 'core/dashboard.html', {'user': user, 'movies1': movies_obj[:4], 'movies2': movies_obj[4:8], 'movies3': movies_obj[8:12]})

