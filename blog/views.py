from rest_framework import viewsets
from rest_framework import permissions

from .mixins import LikedMixin
from .models import Post
from .serializers import PostSerializer


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
