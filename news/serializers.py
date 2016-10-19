from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Article, Category, View, Like


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'name', 'id')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.StringRelatedField(many=True)
    class Meta:
        model = Article
        fields = ('url', 'id', 'title', 'subhead', 'introduction', 'content', 'author', 'editor', 'photographer', 'cover', 'category', 'create_time', 'views', 'likes', 'is_check')


class ViewSerializer(serializers.HyperlinkedModelSerializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    class Meta:
        model = View
        fields = ('article', 'view_ip')


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    class Meta:
        model = Like
        fields = ('article', 'like_ip')





