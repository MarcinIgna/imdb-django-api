from django import forms
from imdb_api.models.user_model import CustomUser


class UserFormLogin(forms.Form):
    username = forms.CharField(       
        label="Username",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your username"}
        )
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password"}
        )
    )