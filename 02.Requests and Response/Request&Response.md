> 本人普通一本，正值大三,为了能有好的就业，痛定思痛戒掉游戏！鞭策自己至少一周一篇博客

- 学习目标：学校课内基础打扎实，课外学会语言框架，同时提升英语阅读水平
- 学习路线（自拟）：`vue` -> `djangorestframework` -> `goland`
- 毕业前想：用前后端分离建成自己的小站，做一款网络游戏（爱好而已）

### 关于本篇djangorestframwork

内容皆会上传到我的github上：https://github.com/BadbadLoli/django-rest-framework-study

本篇参照官网教程：https://www.django-rest-framework.org/tutorial/2-requests-and-responses/

学习为主，如有纰漏请大神指正

---

这一章节，我们将真正开始介绍`DRF`的核心，让我们先介绍几个基本的构建块

# Request对象

`DRF`通过扩展常用的`HttpRequest`对象，引入了一个新的`Request`对象，提供了更加灵活的请求解析，`Request`对象的核心是`request.data`属性，`request.data`类似于`request.POST`，但对于处理`Web API`更加得心应手

- `request.POST`：只处理表单数据，只适用于`POST`请求
- `request.data`： 处理任意数据，适用于`POST`, `PUT`和`PATCH`请求

# Response对象

`DRF`也提供了一个`Response`对象，它的类型是`TemplateResponse`，它接受未渲染的内容，并使用内容协商来确定要返回给客户端的内容

```python
return Response(data)  # 根据客户端请求呈现内容类型
```

# 状态码

在视图函数中使用`HTTP`数值状态码并不利于阅读，而且很容易会忽略掉错误状态码，DRF为每个状态码都提供了一个更加明显的标识符，例如`HTTP_400_BAD_REQUEST`，使用这些易读的标识符而不是数字状态码是一种好选择

# wrapping API views

drf提供了两种wrapper来编写API视图函数

1. `@api_view`：这个装饰器用来处理**基于函数的视图**
2. `APIView`：这个类用来处理**基于类的视图**

这些`wrapper`提供了一些功能，比如确保在在视图函数中接收`request`实例的时候，向`Response`对象添加上下文，以便进行内容协商

上述`wrapper`同时提供了一些行为，比如在适当的时候返回`405 Method Not Allowed`的响应，当`request.data`里存在非法输入的时候，`wrapper`也会对其当成`ParseError`异常进行处理

# 来次实践

我们现在不再需要用到JSONResponse啦，用新组件来编写新的视图函数吧

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET', 'POST'])
def snippet_list(request):
    # 展示所有或创建一个snippet
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    # 检索，更新或删除一个snippet
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

可以感觉到这与常规的`django`视图没有太大的不同，但现在的代码更加简洁，我们用了`@api_view`的装饰器，还用了更加具体的命名状态码，这使得相应的含义更加明显

注意，我们不再显示地将请求或相应绑定到一个给定的类型，`request.data`可以处理传入的`json`请求，也可以处理其他格式，类似的，我们返回带有数据的`response`对象，还允许`drf`把我们的响应渲染到正确的类型里面。

# 向url添加后缀

我们使用格式后缀可以让我们的`url`处理一种给定格式的`url`，就好比我们的`API`能够处理类似`...com/api/items/4.json`这样的`url`

首先向两个视图添加一个`format`的关键字参数

```python
def snippet_list(request, format=None):
    ...
def snippet_detail(request, pk, format=None):
    ...
```

然后稍微更新一下`url.py`

```python
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

关键在最后一句，我们不需要添加额外的`url`模式，`drf`为我们提供了一种引用特定格式的，非常简单干净的方法

# 开始测试

现在可以运行进行测试了，但与上一章不同的是，如果发送无效的请求，我们有更好的错误处理

