from django.shortcuts import render
from rest_framework import views, generics, status, serializers, viewsets

# Create your views here.
from serializers import DynModelSerializer
from tests.sample.sampleapp.models import Article


class ArticleDynSerializer(DynModelSerializer):
    class Meta:
        model = Article
        fields_param = 'article_fields'
        fields = ['id', 'title', 'created', 'updated', 'content', 'author', ]


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()

    def get_serializer(self, *args, **kwargs):
        context = self.get_serializer_context()
        context['request'] = self.request
        s = ArticleDynSerializer(*args, context=context, **kwargs)
        return s
