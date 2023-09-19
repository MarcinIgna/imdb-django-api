from django import forms


class MovieSearchForm(forms.Form):
    search_term = forms.CharField(
        label='Search for a movie',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search for a movie'})
    )