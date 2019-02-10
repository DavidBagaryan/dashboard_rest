from rest_framework import serializers

from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    tags_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('title', 'description', 'date_pub', 'author_name', 'tags_count', 'tags')

    def get_tags_count(self, obj):
        return obj.tags.count()
