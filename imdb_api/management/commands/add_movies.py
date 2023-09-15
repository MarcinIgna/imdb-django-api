import logging
import os
import time
from ratelimit import limits, sleep_and_retry
import httpx
from django.core.management.base import BaseCommand
import django
import tmdbsimple as tmdb
from imdb_api.models.movie_model import Movie

class Command(BaseCommand):
    help = 'Adds movies to the database from TMDB'

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

    def handle(self, *args, **kwargs):
        logging.basicConfig(filename='database_update.log', level=logging.INFO)

        # Replace 'your_project_name' with your actual project name
        DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")
        django.setup()

        tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

        page = 1
        max_pages = 4  # Set the maximum number of pages to fetch (adjust as needed)
        counter = 0

        while page <= max_pages:
            try:
                top_movies = tmdb.Movies().top_rated(page=page)
                print(f"Fetching page {page} of top-rated movies.")
            except Exception as e:
                logging.error(f"Error fetching top rated movies: {e}")
                raise e

            for movie_info in top_movies['results']:
                if counter >= 80:
                    break

                # Check if the movie already exists in the database
                if Movie.objects.filter(tmdb_id=movie_info['id']).exists():
                    print(f"Movie '{movie_info['title']}' already exists in the database. Skipping.")
                    continue

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
                    print(f"Added movie '{movie_info['title']}' to the database.")
                except Exception as e:
                    logging.error(f"Error creating or getting movie: {e}")
                    continue

                counter += 1
                time.sleep(0.5)

            page += 1
