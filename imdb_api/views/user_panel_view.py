from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

import json
from django.contrib.auth.decorators import login_required


from imdb_api.forms.comment_form import CommentForm
from imdb_api.forms.movie_vote_form import MovieVoteForm
from imdb_api.forms.user_panel_update_form import UserUpdateForm
from imdb_api.models.comment_model import Comment
from imdb_api.models.movie_model import Movie
from imdb_api.models.user_favorite_model import UserFavorite
from imdb_api.models.user_vote_model import MovieVote

from imdb_api.utils import update_movie_vote_average




@login_required
def user_update_profile(request):
    """
    This view is used to update the user's own profile.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            # Redirect to the user's profile page or any other appropriate page
            return redirect("imdb:dashboard")  # Adjust the URL name as needed
        else:
            messages.error(request, 'There was an error in the form. Please correct it.')

    else:
        form = UserUpdateForm(instance=request.user)
    
    # Render the form in the template for users to update their profile
    return render(request, 'core/user_update_profile.html', {'form': form})

class CommentView(View):
    """ 
    This class is used to add, edit and delete comments.
    """
    @login_required
    def post(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()
            return redirect('movie_detail', movie_id=movie_id)
        return render(request, 'movie_detail.html', {'movie': movie, 'form': form})
    @login_required
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            if comment.user == request.user:
                form = CommentForm(request.POST, instance=comment)
                if form.is_valid():
                    form.save()
                    return redirect('movie_detail', movie_id=comment.movie.id)
                return render(request, 'edit_comment.html', {'form': form, 'comment': comment})
            return HttpResponseForbidden("You don't have permission to edit this comment.")
        except Comment.DoesNotExist:
            return HttpResponseNotFound("Comment not found.")
    @login_required
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            if comment.user == request.user:
                movie_id = comment.movie.id
                comment.delete()
                return redirect('movie_detail', movie_id=movie_id)
            return HttpResponseForbidden("You don't have permission to delete this comment.")
        except Comment.DoesNotExist:
            return HttpResponseNotFound("Comment not found.")
        

# it is just how it could work we will see 
@login_required    
def toggle_favorite(request, movie_id):
    """
    This view is used to toggle a movie as favorite for a user.
    """
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_id)
        user = request.user

        try:
            user_favorite = UserFavorite.objects.get(user=user, movie=movie)
            user_favorite.delete()
            is_favorite = False
        except UserFavorite.DoesNotExist:
            UserFavorite.objects.create(user=user, movie=movie)
            is_favorite = True
        print('is_favorite:', is_favorite)
        return JsonResponse({"success": True, "is_favorite": is_favorite})
    else:
        print("User not authenticated")
        return JsonResponse({"success": False, "message": "User not authenticated"})
    
    
 
@login_required
def favorite_movies(request):
    """
    This view is used to see the user's favorite movies.
    """
    if request.user.is_authenticated:
        favorite_movies = UserFavorite.objects.filter(user=request.user).select_related('movie')
        return render(request, 'favorite_movies.html', {'favorite_movies': favorite_movies})
    else:
        return HttpResponseForbidden("You don't have permission to view this page.")

@login_required  
def vote_for_movie(request, movie_id):
    """
    This view is used to add or update a user's vote for a movie.
    """
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON payload

        user_vote = data.get('rating')  # Assuming your JavaScript sends 'rating' in the JSON

        if user_vote is not None and 1 <= user_vote <= 10:
            movie = get_object_or_404(Movie, pk=movie_id)
            movie_vote, created = MovieVote.objects.get_or_create(user=request.user, movie=movie, defaults={'rating': user_vote})
            if not created:
                movie_vote.rating = user_vote
                movie_vote.save()
            update_movie_vote_average(movie)
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

    

