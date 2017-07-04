from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from test_samples.sample.sampleapp import views, views_author

router = DefaultRouter()
router.register('article', views.ArticleViewSet)
router.register('article_limit_fields', views.ArticleViewSetLimitFields)
router.register('author', views_author.AuthorViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
