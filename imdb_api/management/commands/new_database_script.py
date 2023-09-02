import os
from django.core.management.base import BaseCommand
import tmdbsimple as tmdb
from imdb_api.models.movie_model import Movie
from imdb_api.models.person_model import Person
from imdb_api.models.genre_model import Genre

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

class Command(BaseCommand):
    help = 'Fetch top-rated movies from TMDb and store them in the database'

    def handle(self, *args, **kwargs):
        # Fetch top-rated movies from TMDb
        movies = tmdb.Movies()
        top_movies = movies.top_rated()['results']

        # Create Movie objects and save them in the database
        for movie_info in top_movies:
            title = movie_info['title']
            overview = movie_info['overview']
            release_date = movie_info['release_date']
            vote_average = movie_info['vote_average']
            popularity = movie_info['popularity']
            vote_count = movie_info['vote_count']
            adult = movie_info['adult']
            video = movie_info['video']

            Movie.objects.create(
                title=title,
                overview=overview,
                release_date=release_date,
                vote_average=vote_average,
                popularity=popularity,
                vote_count=vote_count,
                adult=adult,
                video = video
            )

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored top-rated movies.'))

top_rated_movies = Movie.objects.all()

# Print the list of top-rated movies
for movie in top_rated_movies:
    print(f"Title: {movie.title}")
    print(f"Overview: {movie.overview}")
    print(f"Release Date: {movie.release_date}")
    print(f"Vote Average: {movie.vote_average}")
    print(f"Popularity: {movie.popularity}")
    print(f"Vote Count: {movie.vote_count}")
    print(f"Adult: {movie.adult}")
    print(f"Video: {movie.video}")