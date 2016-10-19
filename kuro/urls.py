from django.conf.urls import url, include
from rest_framework import routers
from news import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# router.register(r'uncheckarticle', views.UnCheckArticleViewSet)
router.register(r'article', views.ArticleViewSet)
router.register(r'category', views.CategoryViewsSet)
router.register(r'view', views.ViewViewSet)
router.register(r'like', views.LikeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^getip/', views.get_user_ip, name='get_ip'),
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^articlelist/', views.ArticleList.as_view(), name='article-list'),
    url(r'^ueditor/', include('DjangoUeditor.urls'))
]