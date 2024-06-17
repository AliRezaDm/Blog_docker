from django.urls import path
from .views import ArticleList, ArticleDetail, ArticlePreview, search_view, CategoryList


app_name = 'article'

urlpatterns = [

    path ('', ArticleList.as_view(), name="home"),   
    path ('detail/<slug>', ArticleDetail.as_view(), name='detail'),
    path ('category/<slug>', CategoryList.as_view(), name='category_list'),
    path ('search/', search_view, name='search'),
]

