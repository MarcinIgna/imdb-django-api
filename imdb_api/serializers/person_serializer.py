from rest_framework import serializers
from ..models.person_model import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id","tmdb_id",'name']
