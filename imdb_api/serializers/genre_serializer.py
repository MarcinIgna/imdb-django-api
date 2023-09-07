from rest_framework import serializers
from imdb_api.models.genre_model import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id",'name']