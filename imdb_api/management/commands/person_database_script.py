import os
from django.core.management.base import BaseCommand
import tmdbsimple as tmdb
from imdb_api.models.movie_model import Movie
from imdb_api.models.person_model import Person
from imdb_api.models.genre_model import Genre

tmdb.API_KEY = "03170fffae5da3bc45c3bacef187d48c"

class Command(BaseCommand):
    help = 'Fetch people from TMDb and store them in the database'

    def handle(self, *args, **kwargs):
        # Fetch people from TMDb (example: top-rated actors)
        tmdb_people = tmdb.People()
        people_list = tmdb_people.popular()['results']

        # Create Person objects and save them in the database
        for person_info in people_list:
            tmdb_id = person_info['id']
            name = person_info['name']
            biography = person_info.get('biography', '')
            birthdate = person_info.get('birthday', None)
            place_of_birth = person_info.get('place_of_birth', None)
            profile_path = person_info.get('profile_path', None)

            Person.objects.get_or_create(
                tmdb_id=tmdb_id,
                name=name,
                biography=biography,
                birthdate=birthdate,
                place_of_birth=place_of_birth,
                profile_path=profile_path
            )

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored people.'))

# Retrieve all Person records from the database
all_people = Person.objects.all()

# Print the list of people
for person in all_people:
    print(f"ID: {person.tmdb_id}")
    print(f"Name: {person.name}")
    print(f"Biography: {person.biography}")
    print(f"Birthdate: {person.birthdate}")
    print(f"Place of Birth: {person.place_of_birth}")
    print(f"Profile Path: {person.profile_path}")