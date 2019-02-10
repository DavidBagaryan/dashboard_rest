from django.urls import path

from .views import *

urlpatterns = [
    path('list/', ArticleList.as_view(), name='articles_list_url'),
    path('create/', CreateArticle.as_view(), name='create_article_url'),
    path('edit/<str:title>/', EditArticle.as_view(), name='edit_article_url'),
    path('read/<str:title>/', ViewArticle.as_view(), name='edit_article_url'),
    path('delete/<str:title>/', DeleteArticle.as_view(), name='edit_article_url'),
]
