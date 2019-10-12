from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# 创建一个路由器并注册我们的viewsets
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# API url现在由路由器自动确定
urlpatterns = [
    path('', include(router.urls)),
]