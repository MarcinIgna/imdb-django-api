import os
import tmdbsimple as tmdb
from django.core.management.base import BaseCommand
from imdb_api.models.movie_model import Movie
from imdb_api.models.trailer_model import TrailerVideo

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

class Command(BaseCommand):
    help = "Fetch trailer videos from TMDb and store them in the database"

    def handle(self, *args, **options):
        try:
            movies = Movie.objects.all()

            for movie in movies:
                # Fetch trailer videos for each movie using TMDb API
                tmdb_id = movie.tmdb_id
                response = tmdb.Movies(tmdb_id).videos()

                # Process and store trailer videos
                for result in response['results']:
                    trailer_video = TrailerVideo(
                        movie=movie,
                        name=result.get('name', ''),
                        key=result.get('key', ''),
                        site=result.get('site', ''),
                        size=result.get('size', 0),
                        type=result.get('type', ''),
                        official=result.get('official', False),
                        published_at=result.get('published_at', None)
                    )
                    trailer_video.save()

        except Exception as e:
            self.stderr.write(f"An error occurred: {str(e)}")
