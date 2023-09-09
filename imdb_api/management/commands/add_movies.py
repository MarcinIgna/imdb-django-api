import logging
import os
import time
from ratelimit import limits, sleep_and_retry
import httpx
from django.core.management.base import BaseCommand
import django
import tmdbsimple as tmdb

from imdb_api.models.genre_model import Genre
from imdb_api.models.movie_model import Movie
from imdb_api.models.person_model import Person

# python manage.py database_update_script to run this script

class Command(BaseCommand):
    help = 'Updates the database with the top 5 rated movies from TMDB'

    # Rate limit: 50 requests per second
    @sleep_and_retry
    @limits(calls=50, period=1)
    def fetch_tmdb_data(self, url):
        try:
            with httpx.Client() as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logging.error(f"Error fetching data from TMDB: {e}")
            return None

# ...

    def handle(self, *args, **kwargs):
        logging.basicConfig(filename='database_update.log', level=logging.INFO)

        # Replace 'your_project_name' with your actual project name
        DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")
        django.setup()

        tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

        movies = tmdb.Movies()
        try:
            top_movies = movies.top_rated()
        except Exception as e:
            logging.error(f"Error fetching top rated movies: {e}")
            raise e

        # Fetch genres and store them in a list
        genres = tmdb.Genres()
        genres_list = genres.movie_list()['genres']

        counter = 0
        for movie_info in top_movies['results']:
            if counter >= 10:
                break

            # Create or get the movie
            try:
                movie, created = Movie.objects.get_or_create(
                    tmdb_id=movie_info['id'],
                    defaults={
                        'title': movie_info['title'],
                        'overview': movie_info['overview'],
                        'release_date': movie_info['release_date'],
                        'poster_path': movie_info['poster_path'],
                        'backdrop_path': movie_info['backdrop_path'],
                        'original_language': movie_info['original_language'],
                        'original_title': movie_info['original_title'],
                        'popularity': movie_info['popularity'],
                        'vote_average': movie_info['vote_average'],
                        'vote_count': movie_info['vote_count'],
                        'adult': movie_info['adult'],
                        'video': movie_info['video'],
                    }
                )
            except Exception as e:
                logging.error(f"Error creating or getting movie: {e}")
                continue

            # Fetch credits for the current movie
            try:
                movie_credits = self.fetch_tmdb_data(f'https://api.themoviedb.org/3/movie/{movie_info["id"]}/credits?id={movie_info["id"]}')
            except Exception as e:
                logging.error(f"Error fetching credits for movie {movie_info['id']}: {e}")
                continue  # Skip this movie and proceed to the next one

            if movie_credits is None:
                logging.warning(f"No credits found for movie {movie_info['id']}. Skipping.")
                continue  # Skip this movie and proceed to the next one

            # Fetching and populating Person (actors and directors)
            for cast in movie_credits.get('cast', [])[:3]:
                try:
                    actor, created = Person.objects.get_or_create(
                        tmdb_id=cast['id'],
                        defaults={'name': cast['name']}
                    )
                    movie.actors.add(actor)
                except Exception as e:
                    logging.error(f"Error adding actor {cast['id']} to movie {movie_info['id']}: {e}")

            for crew in movie_credits.get('crew', []):
                if crew['job'] == 'Director':
                    try:
                        director, created = Person.objects.get_or_create(
                            tmdb_id=crew['id'],
                            defaults={'name': crew['name']}
                        )
                        movie.directors.add(director)
                    except Exception as e:
                        logging.error(f"Error adding director {crew['id']} to movie {movie_info['id']}: {e}")

            # Fetching and populating Genre
            for genre_id in movie_info.get('genre_ids', []):
                try:
                    genre_name = next((genre['name'] for genre in genres_list if genre['id'] == genre_id), 'Unknown')
                    genre, created = Genre.objects.get_or_create(
                        tmdb_id=genre_id,
                        defaults={'name': genre_name}
                    )
                    movie.genres.add(genre)
                except Exception as e:
                    logging.error(f"Error adding genre {genre_id} to movie {movie_info['id']}: {e}")

            counter += 1
            time.sleep(0.5)

