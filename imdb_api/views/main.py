from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from imdb_api.models.movie_model import Movie
from django.contrib.auth.models import User
from imdb_api.models.genre_model import Genre


def frontpage(request):
    """
    This view is used to display the frontpage.
    """
    movies = Movie.objects.all()
    genre = Genre.objects.all()
    context = {
        'movies7': movies[24:28],
        'movies8': movies[28:32],
        'movies9': movies[32:36],
        'movies10': movies[36:40],
        'movies11': movies[40:44],
        'movies12': movies[44:48],
        'genres': genre
     }
    # print('context:', context)
    return render(request, 'core/frontpage.html', context)

@login_required(login_url='imdb:login')
def dashboard(request):
    """
    This view is used to display the dashboard.
    """
    user = request.user.username
    genre = Genre.objects.all()
    movies_obj = Movie.objects.all()
    context = {
        'user': user,
        'movies1': movies_obj[:4], 'movies2': movies_obj[4:8],
        'movies3': movies_obj[8:12],'movies4': movies_obj[12:16],
        'movies5': movies_obj[16:20],'movies6': movies_obj[20:24],
        'movies13': movies_obj[48:52],
        'movies14': movies_obj[52:56],
        'movies15': movies_obj[56:60],
        'movies16': movies_obj[64:68],
        'movies17': movies_obj[72:76],
        'movies18': movies_obj[76:80],
        'genres': genre,
    }
    return render(request, 'core/dashboard.html', context)

@login_required(login_url='imdb:login')
def admin_dashboard(request):
    """
    This view is used to display the admin dashboard.
    """
    users = User.objects.all()
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    context = {
        'users': users,
        'genres': genres,
        'movies': movies,
    }
    return render(request, 'admin/admin_dashboard.html', context)