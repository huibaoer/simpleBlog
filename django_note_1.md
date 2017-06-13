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
