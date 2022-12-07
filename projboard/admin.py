from django.contrib import admin
from .models.article import Article, User, Subject, Like, View_Article

# Register your models here. # Register your models here.
admin.site.register(Article)
admin.site.register(User)
admin.site.register(Like)
admin.site.register(View_Article)
admin.site.register(Subject)
