from django.db import models

class Genre(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name