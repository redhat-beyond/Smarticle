"""finalProject_g4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from projboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='homepage'),
    # path('/<str:user_nickname>/', views.home_page, name='homepage1'),
    # path('search/', views.search, name='search'),
    path('search/<str:user_nickname>/', views.search, name='search'),
    path('create_article/', views.create_article, name='create_article'),
    path('about/', views.about_page, name='aboutpage'),
    path('my_articles/<str:nickname>/', views.my_articles, name="my_articles"),
    path('signup/', views.sign_up, name='signup'),
    path('article/<str:user_nickname>/<str:article_pk>/', views.show_article, name='show_article'),
    path('article/<str:article_pk>/', views.show_article_for_guest, name='show_article_for_guest'),
    path('edit_article/<str:article_pk>/', views.edit_article, name='edit_article'),
    path('delete_article/<str:article_pk>/', views.delete_article, name='delete_article'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name="login")

]

handler404 = views.error_404
