import tmdbsimple as tmdb
from imdb_api.models.genre_model import Genre
from imdb_api.models.movie_model import Movie
from imdb_api.models.person_model import Person
import time

tmdb.API_KEY = '7aa1455545e820a75e0f83c8287045e1'

movies = tmdb.Movies()
top_movies = movies.top_rated()

counter = 0
for movie_info in top_movies['results']:
    if counter >= 100:
        break

    # Create or get the movie
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

    # Fetch credits for the current movie
    movie_credits = movies.credits(id=movie_info['id'])

    # Add directors
    for crew in movie_credits['crew']:
        if crew['job'] == 'Director':
            director, created = Person.objects.get_or_create(
                tmdb_id=crew['id'],
                defaults={'name': crew['name']}
            )
            movie.directors.add(director)

    # Add actors (limiting to the first 3 for brevity)
    for cast in movie_credits['cast'][:3]:
        actor, created = Person.objects.get_or_create(
            tmdb_id=cast['id'],
            defaults={'name': cast['name']}
        )
        movie.actors.add(actor)

    # Associate genres with the movie
    for genre_info in movie_info.get('genre_ids', []):
        genre, created = Genre.objects.get_or_create(
            tmdb_id=genre_info,
            defaults={'name': 'Unknown'}  # You can provide a default name if needed
        )
        movie.genres.add(genre)

    counter += 1
    time.sleep(0.5)