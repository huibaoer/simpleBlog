# django 学习笔记

## 安装django
登陆官网https://www.djangoproject.com/ 到下载页面
- 方法1 若安装了pip，使用官网推荐方式pip安装
- 方法2 源码安装，页面右侧 latest release：下载最新的django。解压后在django根目录执行命令：python3 setup.py install

## 创建django工程
- 安装好django后终端中会有django-admin命令，跳转到准备创建工程的目录下，执行命令 django-admin startproject myblog
- 创建好工程后可以启动服务，查看效果，跳转到工程根目录（manage.py的同级目录）执行命令：python3 manage.py runserver

## 为创建好的工程添加应用
- 跳转到工程根目录执行命令：python3 manage.py startapp blog
- 将新添加的应用添加到工程设置中
```
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'blog',
  ]
```

## 添加第一个响应
- views.py文件中导入类 from django.http import HttpResponse
- 在views中每个响应都是一个函数，创建响应的函数：
```
  def index(request):
      return HttpResponse("Hello World!")
```
- 配置url，在urls.py中添加配置：
```
  import blog.views

  urlpatterns = [
      url(r'^admin/', admin.site.urls),
      url(r'^index/', blog.views.index),
  ]
```
- 命令行执行命令python3 manage.py runserver，查看经典的 ‘Hello World！’ 吧

## 为blog应用添加自己的urls.py配置文件
- 在根urls.py中引入include
```
  from django.conf.urls import url, include
  from django.contrib import admin

  urlpatterns = [
      url(r'^admin/', admin.site.urls),
      url(r'^blog/', include('blog.urls')),
  ]
```

- 在blog应用下新建urls.py文件，并添加如下代码
```
  from django.conf.urls import url
  from . import views

  urlpatterns = [
      url(r'^index/', blog.views.index),
  ]
```

## 为blog添加Templates
- 在blog根目录下创建Templates目录，在Templates目录下创建blog同名目录（防止同名文件）
- blog目录下创建index.html文件
```
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
  <h1>hello,blog</h1>
  </body>
  </html>
```
- 在views.py中返回render()，即可在浏览器中看到效果
```
  def index(request):
      return render(request, 'blog/index.html')
```
- 使用render()传递参数
  - render()中添加字典参数
  ```
    def index(request):
      return render(request, 'blog/index.html', {'text': 'hello,blog,hahaha'})
  ```
  - index.html中使用render()传递过来的参数
  ```
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h1>{{text}}</h1>
    </body>
    </html>
  ```

## Models
- 在应用根目录下models.py文件下引入models模块，创建类，继承models.Model，该类即是一张表，在该类中创建数据表的字段
```
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=32, default='Title')
    content = models.TextField(null=True)
```

- 将数据模型映射成数据表
命令行中进入manage.py同级目录，执行 python3 manage.py makemigrations app(可选)；再执行 python3 manage.py migrate

- 查看db.sqlite3数据库
可以使用数据库可视化工具查看生成的数据库内容，如navicat。blog_article就是models.py文件下创建的Article类生成的表，在blog_article表中添加一条记录，用于后续查看

- 页面呈现model数据
  - blog下的views.py下返回Article对象，引入models，获取键值为1的对象并返回
  ```
      from django.shortcuts import render
      from django.http import HttpResponse
      from . import models

      def index(request):
          article = models.Article.objects.get(pk=1)
          return render(request, 'blog/index.html', {'article': article})
  ```

  - 修改前端，显示article对象返回的数据
  ```
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h1>{{ article.title }}</h1>
    <h2>{{ article.content }}</h2>
    </body>
    </html>
  ```

## admin
- 配置admin
  - 创建用户 python3 manage.py createsuperuser 创建超级用户
  - 启动服务，登录admin，查看效果
  - 将admin后台修改为中文，在settings.py中修改 LANGUAGE_CODE = 'zh_Hans'
- 配置应用，才能admin下管理应用
  - 在应用下admin.py中引入自身的models模块（或者里面的模型类）
  - 编辑admin.py：admin.site.register(models.Article)
  ```
    from django.contrib import admin
    from . import models

    admin.site.register(models.Article)
  ```
  - 登录admin，可以对数据进行增删改查等操作。同时可以使用数据库视图化工具实时查看数据库中的数据变化
  - 修改数据默认显示的名称，在Article类下添加一个方法，python3使用__str__(self)，python2使用__unicode_(self)
  ```
    class Article(models.Model):
      title = models.CharField(max_length=32, default='Title')
      content = models.TextField(null=True)

      def __str__(self):
          return self.title
  ```

## myblog完善
  - 博客页面设计
    - 博客主页面
      - 文章标题列表，超链接
      - 发表博客按钮（超链接）
      后台代码：
      ```
        def index(request):
          articles = models.Article.objects.all()
          return render(request, 'blog/index.html', {'articles': articles})
      ```
      前段代码：
      ```
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>

        <h1>
            <a href="">新文章</a>
        </h1>
        {% for article in articles %}
            <a href="">{{ article.title }}</a>
            <br/>
        {% endfor %}
        </body>
        </html>
      ```
    - 博客文章内容页面
      - 标题
      - 文章内容
      - 修改文章按钮（超链接）
      首先在Templates目录下，添加article_page.html文件
      ```
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <h1>{{ article.title }}</h1>>
        <br/>
        <h3>{{ article.content }}</h3>>
        <br/><br/>
        <a href="">修改文章</a>
        </body>
        </html>
      ```
      在views.py下添加article_page函数
      ```
        def article_page(request, article_id):
          article = models.Article.objects.get(pk=article_id)
          return render(request, 'blog/article_page.html', {'article': article})
      ```
      最后，urls.py中配置url，并传递article_id参数（使用主键id作为article_id），注意传递article_id参数的正则表达式的写法
      ```
        urlpatterns = [
            url(r'index/', views.index),
            url(r'article/(?P<article_id>[0-9]+)', views.article_page),
        ]
      ```
      添加超链接，实现点击列表页面中文章标题后跳转到指定文章的效果，django的Templates中超链接的写法 href="{% url 'app_namespace:url_name' param %}"
      在根urls.py下，为blog url添加namespace
      ```
        urlpatterns = [
          url(r'^admin/', admin.site.urls),
          url(r'^blog/', include('blog.urls', namespace='blog')),
        ]
      ```
      在blog的urls.py下，为article url添加name
      ```
        urlpatterns = [
            url(r'index/', views.index),
            url(r'article/(?P<article_id>[0-9]+)', views.article_page, name='article_page'),
        ]
      ```
      在index.html中添加超链接
      ```
        <body>

        <h1>
            <a href="">新文章</a>
        </h1>
        {% for article in articles %}
            <a href="{% url 'blog:article_page' article.id %}">{{ article.title }}</a>
            <br/>
        {% endfor %}
        </body>
      ```
    - 博客撰写页面
      - 标题编辑栏
      - 文章内容编辑区域
      - 提交按钮
      首先创建edit_page.html文件
      ```
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <form action="{% url 'blog:edit_action' %}" method="post">{% csrf_token %}
            <label>文章标题
                <input type="text" name="title"/>
            </label>
            <br/>
            <label>文章内容
                <input type="text" name="content">
            </label>
            <br/>
            <input type="submit" value="提交">
        </form>

        </body>
        </html>
      ```
      在views.py中添加编辑页面和提交按钮的函数
      ```
        def edit_page(request):
          return render(request, 'blog/edit_page.html')


        def edit_action(request):
            title = request.POST.get('title', 'TITLE')
            content = request.POST.get('content', 'CONTENT')
            models.Article.objects.create(title=title, content=content)
            articles = models.Article.objects.all()
            return render(request, 'blog/index.html', {'articles': articles})
      ```
      在urls.py中添加相关url
      ```
        urlpatterns = [
            url(r'index/$', views.index),
            url(r'article/(?P<article_id>[0-9]+)/$', views.article_page, name='article_page'),
            url(r'edit/$', views.edit_page, name='edit_page'),
            url(r'edit/action/$', views.edit_action, name='edit_action'),
        ]
      ```
      最后在index.html文件中添加‘新建文章’超链接
      ```
        <a href="{% url 'blog:edit_page' %}">新文章</a>
      ```

      - 文章撰写页面添加修改文章功能
      上面的文章撰写页面实现了，点击index页面的新文章按钮，跳转到文章撰写页面，然后创建新文章。但是博客还需要有修改已有文章的功能，下面完善文章撰写页面，让其拥有修改文章的功能
      思路如下：跳转到文章撰写页面的时候需要传递一个article_id作为参数，当新建文章时，article_id为0；当修改文章时，article_id为该文章的键值id。
        - views.py下，为edit_page，添加article_id参数
        ```
          def edit_page(request, article_id):
            if str(article_id) == '0':
                return render(request, 'blog/edit_page.html')
            article = models.Article.objects.get(pk=article_id)
            return  render(request, 'blog/edit_page.html', {'article': article})
        ```
        - 配置edit_page函数的url，添加参数article_id
        ```
          url(r'edit/(?P<article_id>[0-9]+)/$', views.edit_page, name='edit_page'),
        ```
        - 编辑article_page.html的修改文章超链接，传递参数article_id
        ```
          <a href="{% url 'blog:edit_page' article.id %}">修改文章</a>
        ```
        - 编辑index.html的新建文章超链接，传递参数article_id为0
        ```
          <a href="{% url 'blog:edit_page' 0 %}">新文章</a>  
        ```
        - 在edit_page.html中根据article_id的值区分是新建文章还是修改文章，修改文章需要将文章的内容填写在编辑框内
        ```
          <form action="{% url 'blog:edit_action' %}" method="post">
            {% csrf_token %}
            {% if article %}
                <label>文章标题
                    <input type="text" name="title" value="{{ article.title }}"/>
                </label>
                <br/>
                <label>文章内容
                    <input type="text" name="content" value="{{ article.content }}"/>
                </label>
            {% else %}
                <label>文章标题
                    <input type="text" name="title" "/>
                </label>
                <br/>
                <label>文章内容
                    <input type="text" name="content" "/>
                </label>
            {% endif %}
            <br/>
            <input type="submit" value="提交">
          </form>
        ```

        - 编辑页面点击提交按钮，是新建文章的话就创建新的数据model；是修改文章的话就修改本编文章的数据model。
          - 方法1，同样使用修改url，添加article_id参数的方式判断
          - 方法2，不修改url。通过隐藏的input标签传递article_id
        下面使用方法2来实现，在edit_page.html中添加隐藏的input标签。
        ```
          <form action="{% url 'blog:edit_action' %}" method="post">
            {% csrf_token %}
            {% if article %}
                <input type="hidden" name="article_id" value="{{ article.id }}">
                <label>文章标题
                    <input type="text" name="title" value="{{ article.title }}"/>
                </label>
                <br/>
                <label>文章内容
                    <input type="text" name="content" value="{{ article.content }}"/>
                </label>
            {% else %}
                <input type="hidden" name="article_id" value="0">
                <label>文章标题
                    <input type="text" name="title" "/>
                </label>
                <br/>
                <label>文章内容
                    <input type="text" name="content" "/>
                </label>
            {% endif %}
            <br/>
            <input type="submit" value="提交">
          </form>
        ```

        下面修改views.py的提交按钮的响应函数
        ```
          def edit_action(request):
            title = request.POST.get('title', 'TITLE')
            content = request.POST.get('content', 'CONTENT')
            article_id = request.POST.get('article_id', '0')

            if article_id == '0':
                models.Article.objects.create(title=title, content=content)
                articles = models.Article.objects.all()
                return render(request, 'blog/index.html', {'articles': articles})

            article = models.Article.objects.get(pk=article_id)
            article.title = title
            article.content = content
            article.save()
            return render(request, 'blog/article_page.html', {'article': article})
        ```

## 小技巧
- 过滤器
{{ value | filter }}，例如：{{ article_id | default:'0' }}表示article_id的缺省值为0
- Django shell
python3 manage.py shell 启动Django shell，可以进行调试
- admin
配置admin，更多可参考Django文档
```
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')

admin.site.register(models.Article, ArticleAdmin)
```
