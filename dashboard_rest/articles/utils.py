import json

from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Tag, Article

request_format = 'application/json'


class CreateOrUpdateMixin(View):
    action_update = False
    decoded_data = None
    status_code = None
    article = None
    response_mes = ''

    def post(self, request, title=None):
        if request.META.get('CONTENT_TYPE') != request_format:
            self.make_response('only json data allowed', 400)
        else:
            self.decoded_data = json.loads(request.body.decode('utf-8'))
            if 'article' not in self.decoded_data:
                raise HttpResponseBadRequest('no article data in request')

            try:
                if self.action_update and title:
                    self.update_article(title)
                else:
                    self.make_article()
            except HttpResponseBadRequest as bad_response:
                self.make_response(bad_response, bad_response.status_code)

        return HttpResponse(content=self.response_mes, status=self.status_code)

    def update_article(self, title):
        art_data = self.decoded_data['article']
        search = Article.objects.filter(title__iexact=title)

        if search:
            search.update(**art_data)
            self.article = get_object_or_404(Article, title__iexact=art_data['title'])
            self.save_tags()
            self.result_response()
            if title != self.article.title:
                mes = f'article: "{self.article.title}" ("{title}") has updated'
            else:
                mes = f'article: "{self.article.title}" has updated'
        else:
            mes = f'article: "{title}" not found'

        self.make_response(mes)

    def make_article(self):
        art_data = self.decoded_data['article']
        try:
            self.article = Article(**art_data)
            self.article.save()
        except ValidationError as e:
            self.make_response(e.message)
            self.article = Article.objects.get(title__iexact=art_data['title'])
        else:
            if self.article:
                mes = f'article: "{self.article.title}" has successfully saved'
                self.save_tags()
                self.result_response()
            else:
                mes = f"article \"{art_data['title']}\" not found for editing"

            self.make_response(mes)

    def save_tags(self):
        if self.action_update:
            self.article.tags.all().delete()

        if 'tags' in self.decoded_data and self.decoded_data['tags'] is not None:
            for tag in self.decoded_data['tags']:
                try:
                    tag_model = Tag(**tag)
                    tag_model.save()
                except ValidationError as e:
                    self.make_response(e.message)
                else:
                    self.make_response(f'tag #{tag_model.name} has successfully saved')

                self.add_tag(tag)

    def add_tag(self, tag):
        tag_model = get_object_or_404(Tag, name__iexact=tag['name'])
        self.article.tags.add(tag_model)

    def result_response(self):
        tag_mask = '#{}, '
        tags = ''
        suffix = 'saved' if not self.action_update else 'updated'
        existing_tags = list(self.article.tags.all())

        if len(existing_tags):
            last_tag = existing_tags.pop()
            for tag in existing_tags:
                tags += tag_mask.format(tag)
            tags += tag_mask.format(last_tag)[:-2]

        tags = '//no appended tags yet//' if tags == '' else tags

        mes = f'article: "{self.article.title}" with tags: {tags} has {suffix}'
        self.make_response(mes)

    def make_response(self, mes, code=200):
        self.response_mes += f'{mes}\n'
        self.status_code = code
