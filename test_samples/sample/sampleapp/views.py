from rest_framework import viewsets

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
        s = ArticleDynSerializer(*args, context=context, limit_fields=True, **kwargs)
        return s


class LimitFieldsArticle(DynModelSerializer):
    author = AuthorDynSerializer(required=False, limit_fields=True)

    class Meta:
        model = Article
        fields_param = 'article_fields'
        fields = ['id', 'title', 'created', 'updated', 'content', 'author']
        limit_fields = True


class ArticleViewSetLimitFields(viewsets.ReadOnlyModelViewSet):
    serializer_class = LimitFieldsArticle
    queryset = Article.objects.all().order_by('id')
