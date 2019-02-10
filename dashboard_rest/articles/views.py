from django.core import serializers
from django.http import HttpResponse
from django.views import View

from .utils import CreateOrUpdateMixin
from .models import Article

request_format = 'application/json'


# list
class ArticleList(View):
    response_format = 'json'
    fields = ('title', 'description', 'date_pub', 'author_name', 'tags')

    def get(self, request):
        resp = serializers.serialize(self.response_format, Article.objects.all(), fields=self.fields)
        return HttpResponse(resp)


# creates
class CreateArticle(CreateOrUpdateMixin):
    pass


class EditArticle(CreateOrUpdateMixin):
    action_update = True
