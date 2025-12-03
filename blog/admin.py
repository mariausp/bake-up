# blog/admin.py
from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_filter = ("created_at", "categories")
    search_fields = ("title", "description")
    filter_horizontal = ("categories", "likes")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    list_filter = ("created_at",)
    search_fields = ("post__title", "author__username", "text")
