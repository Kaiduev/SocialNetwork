from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import services as likes_services
from .models import Post, Like

User = get_user_model()


class FanSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email',
                  'first_name', 'last_name',
                  'bio', 'last_login',
                  'last_visit')


class PostSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()
    author = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'image',
            'description', 'created_at',
            'is_fan', 'total_likes'
        )

    def get_is_fan(self, obj) -> bool:
        """Check if a `request.user` has liked this post (`obj`)"""
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class LikeByDaySerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()
    likes = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ('date', 'likes')
