from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework_dyn_serializer import DynModelSerializer
from test_samples.sample.sampleapp.models import Review


class UserDynSerializer(DynModelSerializer):
    class Meta:
        model = get_user_model()
        fields_param = 'user_fields'
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        limit_fields = True


class ReviewDynSerializer(DynModelSerializer):
    user = UserDynSerializer(fields=['id', 'first_name', 'last_name'])

    class Meta:
        model = Review
        fields_param = 'review_fields'
        fields = ['id', 'summary', 'content', 'stars', 'article', 'user']
        limit_fields = True


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewDynSerializer
    queryset = Review.objects.all()
