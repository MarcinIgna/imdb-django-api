from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class MovieVoteForm(forms.Form):
    rating = forms.DecimalField(
        validators=[
            MinValueValidator(0.0, message='Vote must be at least 0.0'),
            MaxValueValidator(10.0, message='Vote must be at most 10.0')
        ]
    )