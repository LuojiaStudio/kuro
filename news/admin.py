#coding:utf-8
from django.contrib import admin
from .models import Article, Category, View, Like


class ArticleAdmin(admin.ModelAdmin):
    """
    编辑管理Article
    """
    list_display = ('title', 'id', 'author', 'editor', 'create_time')
    exclude = ('views', 'likes', 'create_time', 'is_check')

    class Meta:
        model = Article


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

    class Meta:
        model = Category

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(View)
admin.site.register(Like)
