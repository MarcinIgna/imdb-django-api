from django.db import models
from imdb_api.models.movie_model import Movie  # Import your Movie model

class TrailerVideo(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    size = models.IntegerField()
    type = models.CharField(max_length=255)
    official = models.BooleanField()
    published_at = models.DateTimeField()

    def __str__(self):
        return self.name
