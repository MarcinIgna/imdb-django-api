from imdb_api.models.genre_model import Genre
from django import forms


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'