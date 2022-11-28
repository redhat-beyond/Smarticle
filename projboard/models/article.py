from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from .subject import Subject
from .user import User


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

    def __str__(self):
        return self.title

    def PartOfTitle(self, Charlen):
        """Returns a part of the title => useful for displaying article """
        if len(self.title) <= Charlen:
            return self.title
        return '%s...' % (self.title[:Charlen])

    def PartOfContent(self, Charlen):
        """Returns a part of the content => useful for displaying article """
        if len(self.content) <= Charlen:
            return self.content
        return '%s...' % (self.content[:Charlen])

    def Edit(self, title=None, content=None, subject=None):
        """
        Updating an Article:
        note : arg subject should be an object that is saved in db
        """
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        # Should check this function
        if subject is not None and subject in Subject.objects.all():
            self.subject_id = subject
        self.save()

    @staticmethod
    def searchByTitle(title):
        """ search of articles by title ( case insensitive ) """
        return Article.objects.filter(title__icontains=title).order_by('title')

    @staticmethod
    def searchBySubject(subject):
        try:
            articles = Article.objects.filter(subject_id=subject).order_by('title')
        except ObjectDoesNotExist:
            return None
        return articles

    @staticmethod
    def searchByUser(user):
        # Return all User articles
        try:
            articles = Article.objects.filter(user_id=user).order_by('date')
        except ObjectDoesNotExist:
            return None
        return articles

    @staticmethod
    def filterByLikes():
        x = [(Article.objects.get(id=i['article_id']), i['num_likes']) for i in Like.objects.values(
                'article_id').annotate(num_likes=Count('article_id')).order_by('num_likes')]
        temp = [i[0] for i in x]
        x.extend([(i, 0) for i in Article.objects.all() if i not in temp])
        return x

    def numOfLikes(self):
        try:
            res = Like.objects.filter(article_id=self).values(
                'article_id').annotate(num_likes=Count('article_id')).values('num_likes')[0]['num_likes']

        except Exception:
            res = 0
        return res

    @staticmethod
    def filterByViews():
        x = [(Article.objects.get(id=i['article_id']), i['num_views']) for i in View.objects.values(
                'article_id').annotate(num_views=Count('article_id')).order_by('num_views')]

        x.extend([(i, 0) for i in Article.objects.all() if i not in x])
        return x

    def numOfViews(self):
        try:
            res = View.objects.filter(article_id=self).values(
                'article_id').annotate(num_views=Count('article_id')).values('num_views')[0]['num_views']

        except Exception:
            res = 0
        return res

    @staticmethod
    def get_article_by_user(user):
        """
        Method return the first article of user (order by date)
        :param user: the User to search
        :return: Article object
        """
        try:
            article = Article.objects.filter(user_id=user).order_by('date').first()
        except ObjectDoesNotExist:
            return None
        return article


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
