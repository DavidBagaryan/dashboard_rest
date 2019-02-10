from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ArticleSerializer
from .utils import CreateOrUpdateMixin
from .models import Article

request_format = 'application/json'


class ArticleList(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({'articles_amount': len(list(articles)), 'articles': serializer.data})


class CreateArticle(CreateOrUpdateMixin):
    pass


class EditArticle(CreateOrUpdateMixin):
    action_update = True


class ViewArticle(APIView):
    def get(self, request, title):
        articles = Article.objects.filter(title__iexact=title)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class DeleteArticle(APIView):
    authentication_classes = []

    def delete(self, request, title):
        article = get_object_or_404(Article, title__iexact=title)
        article.delete()
        return Response(data=f'article: "{title}" was successfully deleted')
