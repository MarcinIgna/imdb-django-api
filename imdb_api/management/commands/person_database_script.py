import os
import tmdbsimple as tmdb
from tmdbsimple import People
from imdb_api.models.person_model import Person
from imdb_api.models.movie_model import Movie
from django.core.management.base import BaseCommand

# Set your TMDB API key
tmdb.API_KEY = os.environ.get('TMDB_API_KEY')


class MovieCredits(People):
    def movie_credits(self, **kwargs):
        path = self._get_id_path('movie_credits')
        tmdb_id = kwargs.get('id', None)
        url = f"https://api.themoviedb.org/3/person/{tmdb_id}/movie_credits"
        kwargs.pop("id", None)
        response = self._GET(url, kwargs)
        self._set_attrs_to_values(response)
        return response
    

class Command(BaseCommand):
    help = 'Fetch people from TMDb and store them in the database with movie credits'

    def handle(self, *args, **kwargs):
        # Fetch people from TMDb (example: top-rated actors)
        tmdb_people = MovieCredits()
        people_list = tmdb_people.popular()['results']

        # Loop through people and add them to the database
        for person_info in people_list:
            tmdb_id = person_info['id']
            name = person_info['name']
            print(name)
            print(tmdb_id)

            # Create or get the Person
            person, created = Person.objects.get_or_create(
                tmdb_id=tmdb_id,
                defaults={
                    'name': name,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added {name} to the database.'))

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
                            }
                        )
                        # Add the Person to the movie's actors
                        movie.actors.add(person)

                if 'crew' in movie_credits:
                    for movie_info in movie_credits['crew']:
                        if movie_info.get('job') == 'Director':
                            # Create or get the Movie
                            movie, created = Movie.objects.get_or_create(
                                tmdb_id=movie_info['id'],
                                defaults={
                                    'title': movie_info['title'],
                                }
                            )
                            # Add the Person to the movie's directors
                            movie.directors.add(person)

            except Exception as e:
                # Handle exceptions
                self.stderr.write(self.style.ERROR(f"Error while fetching movie credits for person {name}: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored people and their movie credits.'))


# import os
# from django.core.management.base import BaseCommand
# import tmdbsimple as tmdb
# from requests.exceptions import HTTPError  # Import the HTTPError class
# from imdb_api.models.movie_model import Movie
# from imdb_api.models.person_model import Person

# tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

# class Command(BaseCommand):
#     help = 'Fetch people from TMDb and store them in the database'

#     def handle(self, *args, **kwargs):
#         # Fetch people from TMDb (example: top-rated actors)
#         tmdb_people = tmdb.People()
#         people_list = tmdb_people.popular()['results']

#         # Create Person objects and save them in the database
#         for person_info in people_list:
#             tmdb_id = person_info['id']
#             name = person_info['name']
#             biography = person_info.get('biography', '')
#             birthdate = person_info.get('birthday', None)
#             place_of_birth = person_info.get('place_of_birth', None)
#             profile_path = person_info.get('profile_path', None)

#             # Create or get the Person
#             person, created = Person.objects.get_or_create(
#                 tmdb_id=tmdb_id,
#                 defaults={
#                     'name': name,
#                     'biography': biography,
#                     'birthdate': birthdate,
#                     'place_of_birth': place_of_birth,
#                     'profile_path': profile_path
#                 }
#             )

#             # Fetch and add credits for movies if available
#             try:
#                 movie_credits = tmdb_people.movie_credits(id=tmdb_id)
#                 if 'cast' in movie_credits:
#                     for movie_info in movie_credits['cast']:
#                         # Create or get the Movie
#                         movie, created = Movie.objects.get_or_create(
#                             tmdb_id=movie_info['id'],
#                             defaults={
#                                 'title': movie_info['title'],
#                                 # Add other movie fields as needed
#                             }
#                         )
#                         # Add the Person to the movie's actors
#                         movie.actors.add(person)
#             except HTTPError as e:
#                 # Handle HTTP errors like 404 (Not Found)
#                 if e.response.status_code == 404:
#                     self.stderr.write(self.style.WARNING(f"Movie credits not found for person {person.name} (ID: {tmdb_id})."))
#                 else:
#                     self.stderr.write(self.style.WARNING(f"HTTP Error while fetching movie credits for person {person.name}: {e}"))
#             except Exception as e:
#                 # Handle other exceptions
#                 self.stderr.write(self.style.WARNING(f"Error while fetching movie credits for person {person.name}: {e}"))

#         self.stdout.write(self.style.SUCCESS('Successfully fetched and stored people and their movie credits.'))




# import os
# from django.core.management.base import BaseCommand
# import tmdbsimple as tmdb
# from imdb_api.models.movie_model import Movie
# from imdb_api.models.person_model import Person
# from imdb_api.models.genre_model import Genre

# tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

# class Command(BaseCommand):
#     help = 'Fetch people from TMDb and store them in the database'

#     def handle(self, *args, **kwargs):
#         # Fetch people from TMDb (example: top-rated actors)
#         tmdb_people = tmdb.People()
#         people_list = tmdb_people.popular()['results']

#         # Create Person objects and save them in the database
#         for person_info in people_list:
#             tmdb_id = person_info['id']
#             name = person_info['name']
#             biography = person_info.get('biography', '')
#             birthdate = person_info.get('birthday', None)
#             place_of_birth = person_info.get('place_of_birth', None)
#             profile_path = person_info.get('profile_path', None)

#             Person.objects.get_or_create(
#                 tmdb_id=tmdb_id,
#                 name=name,
#                 biography=biography,
#                 birthdate=birthdate,
#                 place_of_birth=place_of_birth,
#                 profile_path=profile_path
#             )

#         self.stdout.write(self.style.SUCCESS('Successfully fetched and stored people.'))

# # Retrieve all Person records from the database
# all_people = Person.objects.all()

# # Print the list of people
# for person in all_people:
#     print(f"ID: {person.tmdb_id}")
#     print(f"Name: {person.name}")
#     print(f"Biography: {person.biography}")
#     print(f"Birthdate: {person.birthdate}")
#     print(f"Place of Birth: {person.place_of_birth}")
#     print(f"Profile Path: {person.profile_path}")