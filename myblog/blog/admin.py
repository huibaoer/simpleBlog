from django.contrib import admin
from . import models

admin.site.register(models.Article)


"""
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')

admin.site.register(models.Article, ArticleAdmin)
"""
