import os
from django.core.management.base import BaseCommand
import tmdbsimple as tmdb
from imdb_api.models.movie_model import Movie
from imdb_api.models.person_model import Person
from imdb_api.models.genre_model import Genre

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

class Command(BaseCommand):
    help = 'Fetch genres from TMDb and store them in the database'

    def handle(self, *args, **kwargs):
        # Fetch genres from TMDb
        tmdb_genres = tmdb.Genres()
        genre_list = tmdb_genres.movie_list()['genres']

        # Create Genre objects and save them in the database
        for genre_info in genre_list:
            tmdb_id = genre_info['id']
            name = genre_info['name']

            Genre.objects.get_or_create(
                tmdb_id=tmdb_id,
                name=name
            )

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored genres.'))

# Retrieve all genres from the database
all_genres = Genre.objects.all()

# Print the list of genres
for genre in all_genres:
    print(f"ID: {genre.tmdb_id}, Name: {genre.name}")