from django.urls import path

from .views import *

urlpatterns = [
    path('list/', ArticleList.as_view(), name='articles_list_url'),
    path('create/', CreateArticle.as_view(), name='create_article_url'),
    path('edit/', EditArticle.as_view(), name='edit_article_url'),
    # path('read/', EditArticle.as_view(), name='edit_article_url'),
    # path('delete/', EditArticle.as_view(), name='edit_article_url'),
]
