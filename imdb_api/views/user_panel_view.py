from django.contrib.auth.models import User
from imdb_api.models.genre_model import Genre
from imdb_api.models.movie_model import Movie
from django.views.generic import FormView
from django.template.response import TemplateResponse
from imdb_api.forms.genre_form import GenreForm
from imdb_api.forms.movie_form import MovieForm
from django.shortcuts import render, redirect

# all code for user panel
class UserView(FormView):
    @staticmethod
    def see_all_genres(request):
        genres = Genre.objects.all()
        context = {"genres": genres}
        return TemplateResponse(request, "genre/all_genres.html", context)
    @staticmethod
    def add_genre(request):
        if request.method == 'POST':
            form = GenreForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('see_all_genres')
    @staticmethod
    def see_all_movies(request):
        movies = Movie.objects.all()
        context = {"movies": movies}
        return TemplateResponse(request, "movie/all_movies.html", context)
    def add_movie(request):
        if request.method == 'POST':
            form = MovieForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('see_all_movies')
        else:
            form = MovieForm()
        return render(request, 'movie/movie_form.html', {'form': form})