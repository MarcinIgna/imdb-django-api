from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseForbidden, HttpResponseNotFound


from imdb_api.models.movie_model import Movie
from imdb_api.forms.comment_form import CommentForm
from imdb_api.models.comment_model import Comment


class CommentView(View):
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
