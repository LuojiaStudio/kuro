from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import generics
from news.serializers import UserSerializer, GroupSerializer, ArticleSerializer, CategorySerializer
from .models import Article, Category
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [TokenHasReadWriteScope, ]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class UnCheckArticleViewSet(viewsets.ModelViewSet):
#
#     queryset = Article.objects.filter(is_check=False)
#     serializer_class = ArticleSerializer
#     # permission_classes = [
#     #     IsAuthenticated,
#     #     TokenHasScope,
#     # ]
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (BasicAuthentication,)
#
#     def perform_create(self, serializer):
#         serializer.save(is_check=False)


class ArticleList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Articles to be viewed or edited.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated, )
    required_scopes = ['read']
    authentication_classes = (BasicAuthentication,)


class CategoryViewsSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

