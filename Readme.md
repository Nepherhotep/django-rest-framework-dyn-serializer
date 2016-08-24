# DRF Dynamic Model Serializer [![Build Status](https://travis-ci.org/Nepherhotep/django-rest-framework-dyn-serializer.svg?branch=master)](https://travis-ci.org/Nepherhotep/django-rest-framework-dyn-serializer)

## Intro

Dynamic model serializer designed to create more dynamic REST.
Despite spherical REST in vacuum works with the full models,
very often it's really inconvenient to fetch from database and pass to user
the full instance. It leads to overhead or to having multiple views with different
attribute sets.
Having ability to specify REST endpoint which attributes to return on demand, allows
us to reuse same endpoint in different cases. In some manner it's a simple replacement
of GraphQL.

## Installation

```
pip install rest_framework_dyn_serializer
```

Important! Serializer API may change in future, so always freeze version in requirements.txt:

Good: 
```
rest_framework_dyn_serializer==1.0.0
```

Bad:
```
rest_framework_dyn_serializer
```

Actually, it makes sense for other libraries as well, just a reminder.

## Usage

### Define models
```
from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True, null=True)


class Article(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name='articles')
```

### Define serializer
```
from django.shortcuts import render
from rest_framework import views, generics, status, serializers, viewsets

# Create your views here.
from rest_framework_dyn_serializer import DynModelSerializer
from test_samples.sample.sampleapp.models import Article, Author, Review


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
```

### Set view or viewset to use dynamic serializer
```
class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all().order_by('id')

    def get_serializer(self, *args, **kwargs):
        context = self.get_serializer_context()
        context['request'] = self.request
        s = ArticleDynSerializer(*args, context=context, limit_fields=True, **kwargs)
        return s
```
