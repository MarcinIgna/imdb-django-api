from django.views.generic import FormView
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

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
        This view is used to update the profile of any user by id.
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
        return render(request, "admin/admin_update_profile.html", {"form": form, "user": user})
    
    @staticmethod
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def delete_user(request, user_id):
        """
        This view is used to delete a user by id.
        """
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            user.delete()
            messages.success(request, 'The user has been deleted successfully.')
            return redirect('imdb:see_all_users')
        else:
            context = {'user': user}
            return TemplateResponse(request, 'admin/delete_user.html', context)
    

    @staticmethod
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def see_all_users(request):
        """
        This view is used to see all users and to delete.
        """
        users = User.objects.all()
        if request.method == 'POST':
            user_ids = request.POST.getlist('user_ids')
            users = User.objects.filter(id__in=user_ids)
            users.delete()
            messages.success(request, 'The selected users have been deleted successfully.')
            return redirect('imdb:see_all_users')
        return render(request, "admin/all_users.html", {"users": users})

    @staticmethod
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def see_all_genres(request):
        """
        This view is used to see all genres and to delete.
        """
        genres = Genre.objects.all()
        if request.method == 'POST':
            genre_ids = request.POST.getlist('genre_ids')
            genres = Genre.objects.filter(id__in=genre_ids)
            genres.delete()
            messages.success(request, 'The selected genres have been deleted successfully.')
            return redirect('imdb:see_all_genres')
        context = {"genres": genres}
        return TemplateResponse(request, "admin/all_genres.html", context)
    
    @staticmethod
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def add_genre(request):
        """
        This view is used to add a new genre.
        """
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
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def delete_genre(request, genre_id):
        """
        This view is used to delete a genre by id.
        """
        genre = get_object_or_404(Genre, id=genre_id)
        if request.method == 'POST':
            genre.delete()
            messages.success(request, 'The genre has been deleted successfully.')
            return redirect('imdb:see_all_genres')
 
        else:
            context = {'genre': genre}
            return TemplateResponse(request, 'admin/del_genre.html', context)
        
    @staticmethod
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def see_all_movies(request):
        """
        This view is used to see all movies and to delete.
        """
        if request.method == 'POST':
            movie_ids = request.POST.getlist('movie_ids')
            movies = Movie.objects.filter(id__in=movie_ids)
            movies.delete()
            messages.success(request, 'The selected movies have been deleted successfully.')
            return redirect('imdb:see_all_movies')
        movies = Movie.objects.all()
        return render(request, "admin/all_movies.html", {"movies": movies})
    
    @staticmethod
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def add_movie_not_authomatic(request):
        """
        This view is used to add a new movie.
        """
        if request.method == 'POST':
            form = MovieForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin/all_movies.html')
        else:
            form = MovieForm()
        return render(request, 'admin/add_movie_na.html', {'form': form})
    
    @staticmethod   
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def update_movie(request, movie_id):
        """
        This view is used to update a movie by id.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                form.save()
                messages.success(request, 'The movie has been updated successfully.')
                return redirect('imdb:see_all_movies')
            else:
                messages.error(request, 'There was an error in the form. Please correct it.')
        else:
            form = MovieForm(instance=movie)
        return render(request, 'admin/update_movie.html', {'form': form, 'movie': movie})
    
    @staticmethod
    @login_required
    @user_passes_test(lambda u: u.is_staff or u.is_superuser)
    def delete_movie_genre(request, genre_id):
        """
        This view is used to delete a genre from a movie.
        """
        genre = get_object_or_404(Genre, id=genre_id)
        if request.method == 'POST':
            # Remove the genre from all movies that have it
            Movie.objects.filter(genres=genre).update(genres=None)
            # Delete the genre
            genre.delete()
            messages.success(request, 'The genre has been deleted successfully.')
            return redirect('imdb:see_all_genres')
        else:
            context = {'genre': genre}
            return TemplateResponse(request, 'admin/delete_movie_genre.html', context)
    
