from django.db import models

class Person(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=255, blank=True, null=True)
    profile_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name