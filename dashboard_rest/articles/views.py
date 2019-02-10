import json

from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Article, Tag


# list
class ArticleList(View):
    response_format = 'json'
    fields = ('title', 'description', 'date_pub', 'author_name', 'tags')

    def get(self, request):
        resp = serializers.serialize(self.response_format, Article.objects.all(), fields=self.fields)
        return HttpResponse(resp)


# creates
class CreateArticle(View):
    request_format = 'application/json'
    decoded_data = None
    status_code = None
    article = None
    response_mes = ''

    def make_response(self, mes, code=200):
        self.response_mes += f'{mes}\n'
        self.status_code = code

    def result_response(self):
        tag_mask = '#{}, '
        tags = ''
        existing_tags = list(self.article.tags.all())
        last_tag = existing_tags.pop()

        for tag in existing_tags:
            tags += tag_mask.format(tag)
        tags += tag_mask.format(last_tag)[:-2]

        mes = f'article: "{self.article.title}" with tags: {tags} has saved'
        self.make_response(mes)

    def add_tag(self, tag):
        if self.article is None:
            self.article = get_object_or_404(Article, title__iexact=self.decoded_data['article']['title'])

        tag_model = get_object_or_404(Tag, name__iexact=tag['name'])
        self.article.tags.add(tag_model)

    def save_tags(self):
        tag_data = self.decoded_data['tag']
        if tag_data is not None:
            for tag in tag_data:
                try:
                    tag_model = Tag(**tag)
                    tag_model.save()
                except ValidationError as e:
                    self.make_response(e.message)
                else:
                    self.make_response(f'tag #{tag_model.name} has successfully saved')

                self.add_tag(tag)

        return False

    def create_article(self):
        if not self.decoded_data['article']:
            self.make_response('no article data in request', 400)
            return False

        try:
            art_model = Article(**self.decoded_data['article'])
            art_model.save()
        except ValidationError as e:
            self.make_response(e.message)
            return False
        else:
            self.article = art_model
            self.make_response('article has successfully saved')

    def post(self, request):
        if request.META.get('CONTENT_TYPE') != self.request_format:
            self.make_response('only json data allowed', 400)
        else:
            self.decoded_data = json.loads(request.body.decode('utf-8'))
            self.create_article()
            self.save_tags()
            self.result_response()

        return HttpResponse(content=self.response_mes, status=self.status_code)
