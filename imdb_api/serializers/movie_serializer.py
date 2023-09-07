from rest_framework import serializers
from imdb_api.models.movie_model import Movie
from imdb_api.serializers.genre_serializer import GenreSerializer
from imdb_api.models.genre_model import Genre
from imdb_api.serializers.person_serializer import PersonSerializer
from imdb_api.models.person_model import Person


class MovieSerializer(serializers.ModelSerializer):
    actors = PersonSerializer(many=True)
    directors = PersonSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'overview', 'release_date',
            'poster_path', 'backdrop_path', 'original_language',
            'original_title', 'popularity', 'vote_average', 'vote_count',
            'adult', 'video', 'genres', 'actors', 'directors'
        ]

    def create(self, validated_data):
        genre_data = validated_data.pop('genre', [])
        actors_data = validated_data.pop('actors', [])
        directors_data = validated_data.pop('directors', [])

        movie = super().create(validated_data)

        for genre in genre_data:
            genre_obj, created = Genre.objects.get_or_create(name=genre['name'])
            movie.genres.add(genre_obj)

        for actor_data in actors_data:
            actor, created = Person.objects.get_or_create(**actor_data)
            movie.actors.add(actor)

        for director_data in directors_data:
            director, created = Person.objects.get_or_create(**director_data)
            movie.directors.add(director)

        return movie

    def update(self, instance, validated_data):
        genre_data = validated_data.pop('genre', [])
        actors_data = validated_data.pop('actors', [])
        directors_data = validated_data.pop('directors', [])

        instance = super().update(instance, validated_data)
        instance.genres.clear()
        instance.actors.clear()
        instance.directors.clear()

        for genre in genre_data:
            genre_obj, created = Genre.objects.get_or_create(name=genre['name'])
            instance.genres.add(genre_obj)

        for actor_data in actors_data:
            actor, created = Person.objects.get_or_create(**actor_data)
            instance.actors.add(actor)

        for director_data in directors_data:
            director, created = Person.objects.get_or_create(**director_data)
            instance.directors.add(director)

        return instance



# from rest_framework import serializers
# from imdb_api.models.movie_model import Movie
# from imdb_api.serializers.genre_serializer import GenreSerializer
# from imdb_api.models.genre_model import Genre
# from imdb_api.serializers.person_serializer import PersonSerializer


# class MovieSerializer(serializers.ModelSerializer):
#     actors = PersonSerializer(many=True)
#     directors = PersonSerializer(many=True)
#     genres = GenreSerializer(many=True)

#     class Meta:
#         model = Movie
#         fields = [
#             'id', 'tmdb_id', 'title', 'overview', 'release_date',
#             'poster_path', 'backdrop_path', 'original_language',
#             'original_title', 'popularity', 'vote_average', 'vote_count',
#             'adult', 'video', 'genres', 'actors', 'directors'
#         ]

#     def create(self, validated_data):
#         genre_data = validated_data.pop('genre', [])
#         book = super().create(validated_data)
#         for genre in genre_data:
#             genre_obj, created = Genre.objects.get_or_create(name=genre['name'])
#             book.genre.add(genre_obj)
#         return book
#     def update(self, instance, validated_data):
#         genre_data = validated_data.pop('genre', [])
#         instance = super().update(instance, validated_data)
#         instance.genre.clear()
#         for genre in genre_data:
#             genre_obj, created = Genre.objects.get_or_create(name=genre['name'])
#             instance.genre.add(genre_obj)
#         return instance