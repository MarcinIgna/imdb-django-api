from django.db import models
from django.contrib.auth.models import User
from .movie_model import Movie

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.user.username} commented {self.movie.title}"