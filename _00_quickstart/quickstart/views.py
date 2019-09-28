from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer


class UserViewset(viewsets.ModelViewSet):
    # 允许查看和编辑users
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewset(viewsets.ModelViewSet):
    # 允许查看和编辑groups
    queryset = Group.objects.all()
    serializer_class = GroupSerializer