from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True

    def clean_password(self):
        """
        Hash the password entered by the user.
        """
        password = self.cleaned_data.get('password')
        if password:
            password = make_password(password)
        return password