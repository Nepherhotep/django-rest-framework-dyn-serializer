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


class Review(models.Model):
    summary = models.CharField(max_length=255)
    content = models.TextField()
    stars = models.IntegerField()
    user = models.ForeignKey(User, null=True, blank=True)
    article = models.ForeignKey(Article, related_name='reviews')
