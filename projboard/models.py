from django.db import models
from django.utils import timezone


class Subject(models.Model):
    """
    Subject model

    name- A string, the subject name
    """
    name = models.CharField(max_length=100)


class User(models.Model):
    """
    User model

    email- User's Email
    password- User's password
    name- User's name
    nickname- User's nickname
    """
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=70)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, unique=True)


class Article(models.Model):
    """
    Article model

    user_id- FK to User model
    title- A string, the title of article
    subject_id- FK to Subject model
    content- A string, the content of article
    date- A DateTime object, the date the article created
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    subject_id = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class Like(models.Model):
    """
    Like model

    user_id- FK to User model
    article_id- FK to Article model
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)


class View(models.Model):
    """
    View model

    user_id- FK to User model
    article_id- FK to Article model
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
