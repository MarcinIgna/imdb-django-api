import os
import tmdbsimple as tmdb
from requests.exceptions import HTTPError
from imdb_api.models.movie_model import Movie
from imdb_api.models.person_model import Person
from django.core.management.base import BaseCommand

# Set your TMDB API key
tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

class Command(BaseCommand):
    help = 'Add people to movies based on their credits'

    def handle(self, *args, **kwargs):
        # Fetch people from TMDb (example: top-rated actors)
        tmdb_people = tmdb.People()
        people_list = tmdb_people.popular()['results']
        print(people_list)
        
        # Loop through people and add them to movies based on credits
        for person_info in people_list:
            tmdb_id = person_info['id']
            print(tmdb_id)
            name = person_info['name']
            print(name)

            # Fetch and add credits for movies if available
            try:
                # Fetch movie credits for the person
                movie_credits = tmdb_people.movie_credits(id=tmdb_id)
                
                if 'cast' in movie_credits:
                    for movie_info in movie_credits['cast']:
                        # Create or get the Movie
                        movie, created = Movie.objects.get_or_create(
                            tmdb_id=movie_info['id'],
                            defaults={
                                'title': movie_info['title'],
                                # Add other movie fields as needed
                            }
                        )
                        # Add the Person to the movie's actors
                        movie.actors.add(person)
                if 'crew' in movie_credits:
                    for crew in movie_credits['crew']:
                        if crew['job'] == 'Director':
                            # Add the Person to the movie's directors
                            movie.directors.add(person)
            except HTTPError as e:
                # Handle HTTP errors like 404 (Not Found)
                if e.response.status_code == 404:
                    self.stderr.write(self.style.WARNING(f"Movie credits not found for person {name} (ID: {tmdb_id})."))
                else:
                    self.stderr.write(self.style.WARNING(f"HTTP Error while fetching movie credits for person {name}: {e}"))
            except Exception as e:
                # Handle other exceptions
                self.stderr.write(self.style.WARNING(f"Error while fetching movie credits for person {name}: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully added people to movies based on their credits.'))
