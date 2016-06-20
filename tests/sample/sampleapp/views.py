from django.shortcuts import render
from rest_framework import views, generics, status, serializers, viewsets

# Create your views here.
from serializers import DynModelSerializer
from tests.sample.sampleapp.models import Article, Author, Review


class AuthorDynSerializer(DynModelSerializer):
    class Meta:
        model = Author
        fields_param = 'author_fields'
        fields = ['id', 'name', 'birth_date']


class ArticleDynSerializer(DynModelSerializer):
    author = AuthorDynSerializer(required=False)

    class Meta:
        model = Article
        fields_param = 'article_fields'
        fields = ['id', 'title', 'created', 'updated', 'content', 'author']


class ReviewSerializer(DynModelSerializer):
    class Meta:
        model = Review
        fields_param = 'review_fields'
        fields = ['id', 'summary', 'content', 'stars', 'article']


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all().order_by('id')

    def get_serializer(self, *args, **kwargs):
        context = self.get_serializer_context()
        context['request'] = self.request
        s = ArticleDynSerializer(*args, context=context, **kwargs)
        return s
