from django.db import models
from imdb_api.models.genre_model import Genre
from imdb_api.models.person_model import Person

class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=255)
    backdrop_path = models.CharField(max_length=255)
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=255)
    popularity = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.PositiveIntegerField()
    adult = models.BooleanField()
    video = models.BooleanField()
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Person, related_name='acted_in', blank=True)
    directors = models.ManyToManyField(Person, related_name='directed', blank=True)

    def __str__(self):
        return self.title