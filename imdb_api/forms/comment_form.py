from django import forms
from imdb_api.models.comment_model import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
