from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseForbidden, HttpResponseNotFound


from imdb_api.models.movie_model import Movie
from imdb_api.forms.comment_form import CommentForm
from imdb_api.models.comment_model import Comment
from imdb_api.models.user_favorite_model import UserFavorite


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

  
