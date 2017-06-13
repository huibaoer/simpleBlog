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

## 为应用添加自己的urls.py配置文件
