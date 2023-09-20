from django.views.generic import FormView
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test


from imdb_api.models.genre_model import Genre
from imdb_api.forms.genre_form import GenreForm

from imdb_api.models.movie_model import Movie
from imdb_api.forms.movie_form import MovieForm

# all code for admin panel

class AdminView(FormView):
    @staticmethod
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def update_user_profile(request, user_id):
        """
        This view is used to update the profile of any user.
        """
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            form = UserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'The user\'s profile has been updated successfully.')
                # Redirect to the user's profile page or any other appropriate page
                return redirect("imdb:dashboard")  # Adjust the URL name as needed
            else:
                messages.error(request, 'There was an error in the form. Please correct it.')

        else:
            form = UserChangeForm(instance=user)
        
        # Render the form in the template for the admin to update the user's profile
        return render(request, 'admin/admin_update_profile.html', {'form': form})

    @staticmethod
    def see_all_users(request):
        users = User.objects.all()
        return  render(request, "admin/all_users.html", {"users": users})

    @staticmethod
    def see_all_genres(request):
        genres = Genre.objects.all()
        context = {"genres": genres}
        return TemplateResponse(request, "admin/all_genres.html", context)
    
    @staticmethod
    def add_genre(request):
        if request.method == 'POST':
            form = GenreForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('imdb:see_all_genres')
            else:
                # Handle the case where the form is not valid
                context = {'form': form}
                return TemplateResponse(request, 'admin/add_genre.html', context)
        else:
            form = GenreForm()
            context = {'form': form}
            return TemplateResponse(request, 'admin/add_genre.html', context)
        
    @staticmethod
    def see_all_movies(request):
        movies = Movie.objects.all()
        return render(request, "admin/all_movies.html", {"movies": movies})
    
    def add_movie_not_authomatic(request):
        if request.method == 'POST':
            form = MovieForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin/all_movies.html')
        else:
            form = MovieForm()
        return render(request, 'admin/add_movie_na.html', {'form': form})