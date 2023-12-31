from django.contrib.auth import login, authenticate, logout
from imdb_api.forms.login_form import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from imdb_api.models.genre_model import Genre

def login_view(request):
    genre = Genre.objects.all()
    """
    This view is used to login a user/admin.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("User authenticated successfully")
                
                # Check if the user is staff
                if user.is_staff or user.is_superuser:
                    # Redirect to the admin panel for staff users
                    return redirect('imdb:admin_dashboard')  
                else:
                    # Redirect to the logged in page for normal users
                    return redirect('imdb:dashboard') 
                
            else:
                print("Authentication failed")
        else:
            print("Form is not valid")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'genres': genre,'form': form})


def logout_view(request):
    """
    This view is used to logout a user/admin.
    """
    logout(request)
    return redirect('imdb:frontpage')