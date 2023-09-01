# Standard library imports
import logging
import os
import time

# Third-party imports
import django
import tmdbsimple as tmdb

# Local imports
from imdb_api.models.genre_model import Genre
from imdb_api.models.movie_model import Movie
from imdb_api.models.person_model import Person

# Set up logging
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

counter = 0
for movie_info in top_movies['results']:
    if counter >= 100:
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
        movie_credits = movies.credits(id=movie_info['id'])
    except Exception as e:
        logging.error(f"Error fetching credits for movie {movie_info['id']}: {e}")
        continue

    # Add directors
    for crew in movie_credits['crew']:
        if crew['job'] == 'Director':
            try:
                director, created = Person.objects.get_or_create(
                    tmdb_id=crew['id'],
                    defaults={'name': crew['name']}
                )
                movie.directors.add(director)
            except Exception as e:
                logging.error(f"Error adding director {crew['id']} to movie {movie_info['id']}: {e}")

    # Add actors (limiting to the first 3 for brevity)
    for cast in movie_credits['cast'][:3]:
        try:
            actor, created = Person.objects.get_or_create(
                tmdb_id=cast['id'],
                defaults={'name': cast['name']}
            )
            movie.actors.add(actor)
        except Exception as e:
            logging.error(f"Error adding actor {cast['id']} to movie {movie_info['id']}: {e}")

    # Associate genres with the movie
    for genre_info in movie_info.get('genre_ids', []):
        try:
            genre, created = Genre.objects.get_or_create(
                tmdb_id=genre_info,
                defaults={'name': 'Unknown'}  # You can provide a default name if needed
            )
            movie.genres.add(genre)
        except Exception as e:
            logging.error(f"Error adding genre {genre_info} to movie {movie_info['id']}: {e}")

    counter += 1
    time.sleep(0.5)
