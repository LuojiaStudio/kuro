from django.contrib import admin
from .models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'editor', 'create_time')
    exclude = ('views', 'likes', 'create_time', 'is_check')
    class Meta:
        mdoel = Article


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
