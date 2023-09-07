from django.contrib.auth import login, authenticate, logout
from imdb_api.forms.login_form import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
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
                if user.is_staff:
                    # Redirect to the admin panel for staff users
                    return redirect('admin_panel_url_name')  
                else:
                    # Redirect to the logged in page for normal users
                    return redirect('imdb:logged_in') 
                
            else:
                print("Authentication failed")
        else:
            print("Form is not valid")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('imdb:frontpage')