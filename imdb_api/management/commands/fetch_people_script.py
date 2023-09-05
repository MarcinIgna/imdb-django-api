import os
import tmdbsimple as tmdb
from imdb_api.models.person_model import Person
from django.core.management.base import BaseCommand

# Set your TMDB API key
tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

class Command(BaseCommand):
    help = 'Fetch people from TMDb and store them in the database'

    def handle(self, *args, **kwargs):
        # Fetch people from TMDb (example: top-rated actors)
        tmdb_people = tmdb.People()
        people_list = tmdb_people.popular()['results']

        # Loop through people and add them to the database
        