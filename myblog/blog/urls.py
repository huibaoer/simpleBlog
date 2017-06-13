from django.conf.urls import url
import blog.views

urlpatterns = [
    url(r'^index/', blog.views.index),
]