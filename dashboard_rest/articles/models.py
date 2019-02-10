from django.core.exceptions import ValidationError
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=150, db_index=True, unique=True)
    description = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=150, db_index=True)

    tags = models.ManyToManyField('Tag', blank=True, related_name='articles')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if Article.objects.filter(title=self.title).exists():
            raise ValidationError(f'article with title: "{self.title}" already exists')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if Tag.objects.filter(name=self.name).exists():
            raise ValidationError(f'tag with name: #{self.name} already exists')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
