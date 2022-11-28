from django.contrib import admin
from .models.models import Article, User, Subject, Like, View
# Register your models here.

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Like)
admin.site.register(View)
