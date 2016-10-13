from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, filters
from news.serializers import UserSerializer, GroupSerializer, ArticleSerializer, CategorySerializer
from .models import Article, Category
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication


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
    """
    API endpoint that allows Articles to be viewed
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)


class CategoryList(generics.ListAPIView):
    """
    API endpoint that allows Categories to be viewed
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Articles to be viewed or edited.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, TokenHasReadWriteScope)
    # authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('category', 'title')
    search_fields = ('title',)


class CategoryViewsSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, TokenHasReadWriteScope)
    # authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

