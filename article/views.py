from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Article, Category
from .forms import SearchForm

from comment.models import Comment
from comment.forms import CreateCommentForm, ReplyCommentForm


################################################################################################################################

class ArticleList(ListView):
    """
        ClassView for Articles list page
    """
    # model = Article
    template_name = 'article/home.html'
    context_object_name = 'articles'
    queryset = Article.objects.published()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =super().get_context_data(**kwargs)
        context['recent'] = Article.objects.published()[:3]
        return context 

#---------------------------------------------------------------------------------------------------------------------------------#

# def article_list_view(request):
#     """
#         Functional for Articles list page
#     """
#     articles = Article.objects.published()

#     context = {
#         "articles": articles
#     }
    
#     return render(request, 'article/home.html', context)


################################################################################################################################

class ArticleDetail(DetailView):
    """
        ClassView for Article detail page
    """

    model = Article
    context_object_name = 'detail'
    template_name = 'article/detail.html'

    def get_object(self):
        global article_comments
        slug = self.kwargs.get('slug')
        article_comments = Comment.objects.select_related("article", "user").filter(article__slug=slug, is_reply=False)
        return get_object_or_404(Article.objects.published(), slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
               
        context["article_comments"] = article_comments
        context["create_comment_form"] = CreateCommentForm()
        context["reply_comment_form"] = ReplyCommentForm()
        context['recent'] = Article.objects.published()[:3]
        
        return context


#---------------------------------------------------------------------------------------------------------------------------------#

# def article_detail_view(request, slug):
#     """
#         Functional for Articles list page
#     """
#     article_detail = get_object_or_404(Article, slug=slug)
    
#     create_comment_form = CreateCommentForm()
    
#     reply_comment_form = ReplyCommentForm()

#     article_comments = Comment.objects.select_related("article").filter(article__slug=slug, is_reply=False, status="published")

#     context = {
#         'detail': article_detail,
#         'create_comment_form': create_comment_form,
#         'reply_comment_form': reply_comment_form,
#         'article_comments': article_comments,
#     }

#     return render(request, 'article/detail.html',context)


################################################################################################################################

class ArticlePreview(DetailView):
    """
        Classbased for Articles Preview page
    """

    model = Article
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


################################################################################################################################

class CategoryList(ListView):
    """
        Classbased for Category list page
    """

    model = Category
    template_name = 'article/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        context =super().get_context_data(**kwargs)
        context['categories'] = Category.objects.active()
        return context
    

#---------------------------------------------------------------------------------------------------------------------------------#

# def category_list_view(request, slug):
#     """
#         Functional for Category list page
#     """
#     articles = Article.objects.select_related('category').filter(category__slug=slug).order_by('-publish')
    
#     context = {
#         "articles" : articles,
#     }
    
#     return render(request, 'article/home.html', context)


################################################################################################################################

@require_POST
def search_view(request):
    article_query = Article.objects.published()
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data['search']
            if data.isdigit():
                articles = article_query.filter(Q(publish__year=data) | Q(publish__month=data))
            else:
                articles = article_query.filter(Q(title__icontains = data) | Q(description__icontains = data))
            
            return render(request, 'article/home.html', {"articles": articles, "search_form": search_form})


################################################################################################################################

