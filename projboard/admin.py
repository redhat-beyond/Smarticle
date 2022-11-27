from django.contrib import admin
from .models import Article,User,Like,View 

# Register your models here.

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Like)
admin.site.register(View)