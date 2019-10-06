from .models import Snippet
from .serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics


# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     # 展示所有/创造一条snippet
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     # 检索，更新或删除一条snippet实例
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.put(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.delete(request, *args, **kwargs)

class SnippetList(generics.ListAPIView):
    # 展示所有/创造一条snippet
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    # 检索，更新或删除一条snippet实例
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
