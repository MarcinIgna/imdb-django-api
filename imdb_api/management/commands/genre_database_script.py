import os
from django.core.management.base import BaseCommand
import tmdbsimple as tmdb
from imdb_api.models.movie_model import Movie
from imdb_api.models.genre_model import Genre

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

class Command(BaseCommand):
    help = 'Fetch genres from TMDb and associate them with movies in the database'

    def handle(self, *args, **kwargs):
        # Fetch genres from TMDb
        tmdb_genres = tmdb.Genres()
        genre_list = tmdb_genres.movie_list()['genres']

        # Create a dictionary to map genre tmdb_id to genre name
        genre_mapping = {genre_info['id']: genre_info['name'] for genre_info in genre_list}

        # Retrieve all movies from your database
        all_movies = Movie.objects.all()

        for movie in all_movies:
            try:
                # Fetch the movie details from TMDb
                movie_details = tmdb.Movies(movie.tmdb_id).info()
                # Get the list of genre IDs associated with the movie from TMDb
                tmdb_genre_ids = movie_details.get('genres', [])

                # Associate the genres with the movie based on matching tmdb_id values
                for genre_id in tmdb_genre_ids:
                    genre_name = genre_mapping.get(genre_id['id'])
                    if genre_name:
                        genre, created = Genre.objects.get_or_create(
                            tmdb_id=genre_id['id'],
                            name=genre_name
                        )
                        movie.genres.add(genre)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing movie {movie.tmdb_id}: {e}"))
                continue

        self.stdout.write(self.style.SUCCESS('Successfully associated genres with movies.'))

