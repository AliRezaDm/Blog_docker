from django.contrib import admin
from django.db.models import Count, Subquery, OuterRef
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _
from jalali_date.admin import TabularInlineJalaliMixin	

from .models import Article, Category

from comment.models import Comment



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('position', 'title', 'slug', 'parent','status', 'column_category_articles_count')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug':('title',)}

    
    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related("articles").annotate(
            category_articles_count=Count('articles')
        )
        return queryset
    
    @admin.display(ordering="category_articles_count", description=_("# articles"))
    def column_category_articles_count(self, category=Category):
        url = (
            reverse("admin:article_category_changelist")
            + "?"
            + urlencode({
                "category": category.id,
            })
        )
        return format_html('<a href="{}">{}</a>', url, category.category_articles_count)

# admin.site.register(Category, CategoryAdmin)





@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'thumbnail_tag','slug', 'jpublish', 'status', 'category_to_str', 'column_article_comments_count')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'discription')
    prepopulated_fields = {'slug':('title',)}
    ordering =  ['status', 'publish']
    actions = ["make_published", "make_drafted"]

# admin.site.register(Article, ArticleAdmin)
    
    def get_queryset(self, request):
        # Annotate with counts of related Article instances
        queryset = super().get_queryset(request).prefetch_related("comments").annotate(
            article_comments_count=Subquery(
                Comment.objects.filter(article_id=OuterRef('id')).values('article_id').annotate(
                    count=Count('article_id')).values('count'),
                output_field=models.IntegerField()
            ),
        )
        return queryset
    
    @admin.display(ordering="article_comments_count", description=_("# comments"))
    def column_article_comments_count(self, article=Article):
        url = (
            reverse("admin:article_article_changelist")
            + "?"
            + urlencode({
                "article": article.id,
            })
        )
        return format_html('<a href="{}">{}</a>', url, article.article_comments_count)
