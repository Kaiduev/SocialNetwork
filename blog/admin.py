from django.contrib import admin

from .models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_likes', )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'date_of_like', )
