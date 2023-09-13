from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count

from imdb_api.models.movie_model import Movie
from imdb_api.forms.comment_form import CommentForm
from imdb_api.models.comment_model import Comment
from imdb_api.models.user_favorite_model import UserFavorite
from imdb_api.models.user_vote_model import MovieVote
from imdb_api.utils import update_movie_vote_average
from imdb_api.forms.movie_vote_form import MovieVoteForm


def update_user_profile(request):
    """
    This view is used to update the user's profile.
    """
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            # Redirect to the user's profile page or any other appropriate page
            return redirect("user_profile")  # Adjust the URL name as needed
        else:
            messages.error(request, 'There was an error in the form. Please correct it.')

    else:
        form = UserChangeForm(instance=request.user)
    
    # Render the form in the template for users to update their profile
    return render(request, 'profile_update.html', {'form': form})


class CommentView(View):
    """ 
    This view is used to add, edit and delete comments.
    """
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
class UserFavoriteView(View):
    """
    This view is used to add and remove movies from the user's favorites.
    """
    def add_to_favorite(self, request, movie_id):
        if request.user.is_authenticated:
            movie = Movie.objects.get(pk=movie_id)
            user_favorite, created = UserFavorite.objects.get_or_create(user=request.user, movie=movie)
            if created:
                return redirect('movie_detail', movie_id=movie_id)
            else:
                return HttpResponseForbidden("You have already added this movie to your favorites.")
        else:
            return HttpResponseForbidden("You don't have permission to add this movie to your favorites.")
        
    def remove_from_favorite(self, request, movie_id):
        if request.user.is_authenticated:
            movie = Movie.objects.get(pk=movie_id)
            user_favorite = UserFavorite.objects.get(user=request.user, movie=movie)
            user_favorite.delete()
            return redirect('movie_detail', movie_id=movie_id)
        else:
            return HttpResponseForbidden("You don't have permission to remove this movie from your favorites.")
     # View the user's all favorite movies   
    def favorite_movies(self, request):
        if request.user.is_authenticated:
            favorite_movies = UserFavorite.objects.filter(user=request.user).select_related('movie')
            return render(request, 'favorite_movies.html', {'favorite_movies': favorite_movies})
        else:
            return HttpResponseForbidden("You don't have permission to view this page.")

    
  
# check if form is needed if not under is function that is not using form      
def vote_for_movie(request, movie_id):
    """
    This view is used to add or update a user's vote for a movie.
    """
    if request.method == 'POST':
        form = MovieVoteForm(request.POST)
        if form.is_valid():
            user_vote = form.cleaned_data['rating']
            movie = get_object_or_404(Movie, pk=movie_id)
            movie_vote, created = MovieVote.objects.get_or_create(user=request.user, movie=movie, defaults={'rating': user_vote})
            if not created:
                movie_vote.rating = user_vote
                movie_vote.save()
            update_movie_vote_average(movie)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# def vote_for_movie(request, movie_id):
#     """
#     This view is used to add or update a user's vote for a movie.
#     """
#     if request.method == 'POST':
#         user_vote = request.POST.get('rating')  # Assuming the rating is sent in the POST data
#         if user_vote is not None:
#             user_vote = float(user_vote)  # Convert the user's vote to a float if needed
#             movie = get_object_or_404(Movie, pk=movie_id)
#             movie_vote, created = MovieVote.objects.get_or_create(user=request.user, movie=movie, defaults={'rating': user_vote})
#             if not created:
#                 movie_vote.rating = user_vote
#                 movie_vote.save()
#             update_movie_vote_average(movie)
#             return JsonResponse({'success': True})
#     return JsonResponse({'success': False})