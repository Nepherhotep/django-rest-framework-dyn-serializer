from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from tests.sample.sampleapp.views import ArticleViewSet

router = DefaultRouter()
router.register('article', ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
