from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from imdb_api.forms.login_form import UserFromLogin


def login_view(request):
    if request.method == 'POST':
        form = UserFromLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    messages.success(request, 'You have been logged in as staff.')
                    return redirect('admin:index') # admin:index is the admin dashboard 
                else:
                    messages.success(request, 'You have been logged in successfully.')
                    return redirect('home')# user home page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserFromLogin()
    return render(request, 'login.html', {'form': form})