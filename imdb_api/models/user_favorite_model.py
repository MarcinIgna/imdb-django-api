from django.db import models
from django.contrib.auth.models import User
from imdb_api.models.movie_model import Movie  # Import your Movie model

class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} likes {self.movie.title}"