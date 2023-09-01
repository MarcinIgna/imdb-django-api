from django import forms


class UserFromLogin(forms.Form):
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