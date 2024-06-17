from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Comment



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
        We make this class to show our Comment model in admin panel.  
    """
    list_display = ['id', 'user', 'article', 'is_reply', 'status', 'reply_count_column']
    search_fields = ['user__icontains', 'article__icontains', 'content__icontains']
    list_editable = ['status', ]
    list_per_page = 10
    list_select_related = ['user', 'article']
    list_filter = ['status', 'is_reply', 'datetime_create' ]
    autocomplete_fields = ['user', 'article']
    
    
    def get_queryset(self, request):
        """
            We overwrite the default queryset to add prefetch_related and make a new column in Comment model.
        """
        queryset = super(CommentAdmin, self).get_queryset(request)
        return queryset.prefetch_related("comment_replies").annotate(replies_count = Count("comment_replies"))
    
    
    def lookup_allowed(self, key, value):
        """
            We must override this method to use reply as filter for show the comment_replies by using reply_count_column method.
        """
        if key in ('reply'):
            return True
        return super(CommentAdmin, self).lookup_allowed(key, value)
    
    
    @admin.display(ordering="replies_count", description="# replies")
    def reply_count_column(self, comment=Comment):
        """
            We use this method to get the number of comment`s replies in the changelist.
        """
        url = (
            reverse("admin:comment_comment_changelist")
            + "?"
            + urlencode({
                "reply" : comment.id,
            })
        )
        return format_html('<a href="{}" >{}</a>', url, comment.replies_count)

