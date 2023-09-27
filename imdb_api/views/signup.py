from django.shortcuts import render, redirect
from imdb_api.forms.SignUp_form import SignUpForm
from django.contrib.auth import login
from rest_framework.authtoken.models import Token  # Import the Token model

def signup(request):
    """
    This view is used to signup a user.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create a token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            login(request, user)
            return redirect('imdb:login')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})

