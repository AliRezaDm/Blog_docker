from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Comment
from .forms import CreateCommentForm, ReplyCommentForm


@require_POST
def create_comment_view(request, product_id):
    """ 
        This is a functional view for creating a new comment for our product and user can write his/her comments in product_detail.html
    """
    
    url = request.META.get('HTTP_REFERER')
    comment = CreateCommentForm(request.POST)
    if comment.is_valid():
        data = comment.cleaned_data
        
        Comment.objects.create(user_id = request.user.id, product_id = product_id, content = data["content"], rate = data["rate"])

        messages.success(request, "Comment created successfully")
    
    else:        
        messages.warning(request, "Something goes wrong")
        
    return redirect(url)


@require_POST
def reply_comment_view(request, product_id, comment_id):
    """ 
        This is a functional view for reply the comment for our product and user can write his/her comments in product_detail.html
    """
    
    url = request.META.get('HTTP_REFERER')
    comment = ReplyCommentForm(request.POST)
    if comment.is_valid():
        data = comment.cleaned_data
        
        Comment.objects.create(user_id = request.user.id, product_id = product_id, content = data["content"], reply=comment_id, is_reply=True)

        messages.success(request, "Comment reply successfully")
    
    else:        
        messages.warning(request, "Something goes wrong")
        
    return redirect(url)
