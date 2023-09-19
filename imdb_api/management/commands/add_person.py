import os
import tmdbsimple as tmdb
from tmdbsimple import People
from django.core.management.base import BaseCommand

from imdb_api.models.person_model import Person
from imdb_api.models.movie_model import Movie


# Set your TMDB API key
tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

class MovieCredits(People):
    def movie_credits(self, **kwargs):
        tmdb_id = kwargs.get('id', None)
        url: str = f"person/{tmdb_id}/movie_credits"
        kwargs.pop("id", None)
        response = self._GET(url, kwargs)
        self._set_attrs_to_values(response)
        return response


class Command(BaseCommand):
    help = 'Fetch people from TMDb and store them in the database with movie credits'

    def handle(self, *args, **kwargs):
        # Set the number of pages you want to fetch (each page has 20 results)
        num_pages = 2

        for page in range(1, num_pages + 1):
            # Fetch people from TMDb (example: top-rated actors)
            tmdb_people = MovieCredits()
            results = tmdb_people.popular(page=page)['results']
            # Filter out only actors and directors
            people_list = [entry for entry in results if entry.get('known_for_department') in ['Acting', 'Directing']]
        
            # Loop through people and add them to the database if they have played in movies in your database
            for person_info in people_list:
                tmdb_id = person_info['id']
                name = person_info['name']


                try:
                    # Fetch movie credits for the person
                    movie_credits = tmdb_people.movie_credits(id=tmdb_id)

                    if 'cast' in movie_credits:
                        for movie_info in movie_credits['cast']:
                            tmdb_movie_id = movie_info['id']
                            # Check if the movie already exists in your database
                            movie = Movie.objects.filter(tmdb_id=tmdb_movie_id).first()
                            if movie:
                                # Movie exists, create or get the Person and add them to the movie's actors
                                person, _ = Person.objects.get_or_create(
                                    tmdb_id=tmdb_id,
                                    defaults={
                                        'name': name,
                                    }
                                )
                                movie.actors.add(person)

                    if 'crew' in movie_credits:
                        for movie_info in movie_credits['crew']:
                            if movie_info.get('job') == 'Director':
                                tmdb_movie_id = movie_info['id']
                                # Check if the movie already exists in your database
                                movie = Movie.objects.filter(tmdb_id=tmdb_movie_id).first()
                                if movie:
                                    # Movie exists, create or get the Person and add them to the movie's directors
                                    person, _ = Person.objects.get_or_create(
                                        tmdb_id=tmdb_id,
                                        defaults={
                                            'name': name,
                                        }
                                    )
                                    movie.directors.add(person)

                except Exception as e:
                    # Handle exceptions
                    self.stderr.write(self.style.ERROR(f"Error while fetching movie credits for person {name}: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored people and their movie credits.'))


