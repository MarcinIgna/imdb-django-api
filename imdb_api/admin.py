from django.contrib import admin
from imdb_api.models.genre_model import Genre
from imdb_api.models.movie_model import Movie
from imdb_api.models.person_model import Person
from imdb_api.models.trailer_model import TrailerVideo

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(TrailerVideo)

