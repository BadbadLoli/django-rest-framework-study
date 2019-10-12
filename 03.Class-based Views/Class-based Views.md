> 本人普通一本，正值大三,为了能有好的就业，痛定思痛戒掉游戏！鞭策自己至少一周一篇博客

- 学习目标：学校课内基础打扎实，课外学会语言框架，同时提升英语阅读水平
- 学习路线（自拟）：`vue` -> `djangorestframework` -> `goland`
- 毕业前想：用前后端分离建成自己的小站，做一款网络游戏（爱好而已）

### 关于本篇djangorestframwork

内容皆会上传到我的github上：https://github.com/BadbadLoli/django-rest-framework-study

本篇参照官网教程：https://www.django-rest-framework.org/tutorial/3-class-based-views/

学习为主，如有纰漏请大神指正

---

我们可以使用类视图而不是函数视图，这是一个强大的模式，它允许我们重用公共的功能，并帮助我们简化代码

# 用类视图重写我们的视图函数


```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    # 展示所有/创造一条snippet
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    # 检索，更新或删除一条snippet实例
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

既然是基于类的视图，`urls.py`也要进行适当的改变

```
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

# 使用mixins

使用类视图的一大好处是，它可以允许我们轻松的组合各种可重用的行为

我们使用的`create/retrieve/update/delete`这些通用操作，在`drf`里都有对应的`mixin`类实现

```
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

我们使用基类`GenericAPIView`构建视图，并添加了`ListModelMixin`和`CreateModelMixin`，`GenericAPIView`提供核心功能，而`mixin`类提供`.list()`，`.create()`，`.retrieve()`，`.update()`，`.destroy()`操作，然后将其绑定到`get`和`post`请求上

# 使用通用的类视图

通过使用`mixin`类，我们重写了视图，并比之前使用了更少的代码，但是代码可以更加简洁，`drf`给我们提供了一组已经混合了多种`mixin`类的通用视图，用来进一步简化`view.py`

```
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```

哇，真简洁。我们已经获得了大量的资源，我们的代码看起来很好，干净，符合Django的习惯。接下来，我们将进入本教程的第4部分，在这里我们将了解如何处理API的身份验证和权限。
