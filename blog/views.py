import django_filters
from django.db.models import Count
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics

from .mixins import LikedMixin
from .models import Post, Like
from .serializers import PostSerializer, LikeByDaySerializer
from .filters import LikeFilter


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikesView(generics.ListAPIView):
    queryset = Like.objects.extra(select={'date': "date(blog_like.date_of_like)"}).annotate(likes=Count('pk')).order_by('-date_of_like')
    serializer_class = LikeByDaySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filterset_class = LikeFilter
