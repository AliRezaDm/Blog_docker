from django import forms

from .models import Comment


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        
        fields = ['content']


class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        
        fields = ['content']

