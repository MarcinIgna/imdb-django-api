from django.shortcuts import render, redirect
from imdb_api.forms import SignUpForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST': # to know if form has been clicked or submitted
        form = SignUpForm(request.POST)

        # check if valid and password is matching
        if form.is_valid():
            user = form.save() #new user

            login(request, user)

            return redirect('imdb:frontpage')
        
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})
