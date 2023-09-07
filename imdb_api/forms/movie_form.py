from django import forms
from imdb_api.models.movie_model import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'