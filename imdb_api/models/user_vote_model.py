from django.db import models
from django.contrib.auth.models import User
from .movie_model import Movie  # Import your Movie model

class MovieVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()