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

    def part_of_title(self, Charlen):
        """Returns a part of the title => useful for displaying article """
        if len(self.title) <= Charlen:
            return self.title
        return '%s...' % (self.title[:Charlen])

    def part_of_content(self, Charlen):
        """Returns a part of the content => useful for displaying article """
        if len(self.content) <= Charlen:
            return self.content
        return '%s...' % (self.content[:Charlen])

    def edit(self, title=None, content=None, subject=None):
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
    def search_by_title(title):
        """ search of articles by title ( case insensitive ) """
        return Article.objects.filter(title__icontains=title).order_by('title')

    @staticmethod
    def search_by_subject(subject):
        try:
            articles = Article.objects.filter(subject_id=subject).order_by('title')
        except ObjectDoesNotExist:
            return None
        return articles

    @staticmethod
    def search_by_user(user):
        # Return all User articles
        try:
            articles = Article.objects.filter(user_id=user).order_by('date')
        except ObjectDoesNotExist:
            return None
        return articles

    @staticmethod
    def filter_by_likes():
        x = [(Article.objects.get(id=i['article_id']), i['num_likes']) for i in Like.objects.values(
                'article_id').annotate(num_likes=Count('article_id')).order_by('num_likes')]
        temp = [i[0] for i in x]
        x.extend([(i, 0) for i in Article.objects.all() if i not in temp])
        return x

    def num_of_likes(self):
        try:
            res = Like.objects.filter(article_id=self).values(
                'article_id').annotate(num_likes=Count('article_id')).values('num_likes')[0]['num_likes']

        except Exception:
            res = 0
        return res

    @staticmethod
    def filter_by_views():
        x = [(Article.objects.get(id=i['article_id']), i['num_views']) for i in View_Article.objects.values(
                'article_id').annotate(num_views=Count('article_id')).order_by('num_views')]

        x.extend([(i, 0) for i in Article.objects.all() if i not in x])
        return x

    def num_of_views(self):
        try:
            res = View_Article.objects.filter(article_id=self).values(
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

    @staticmethod
    def amount_of_likes_article(article_id):
        """
        Method return the amount of like of one article
        :param article_id: The article to count his likes
        :return: int, the amount of likes
        """
        return Like.objects.filter(article_id=article_id).count()

    @staticmethod
    def create_like(user_id, article_id):
        """
        Method create a new like
        :param user_id: the user that like the article
        :param article_id: the article that the user like
        :return: the like that created
        """
        like = Like(user_id=user_id, article_id=article_id)
        like.save()
        return like

    @staticmethod
    def delete_like(user_id, article_id):
        """
        Method delete a like
        :param user_id: the user that like the article
        :param article_id: the article that the user like
        :return: True if success
        """
        try:
            like = Like.objects.get(user_id=user_id, article_id=article_id)
            like.delete()
            return True
        except Like.DoesNotExist:
            return False

    def __str__(self):
        return f"{self.user_id.name} Liked {self.article_id.title}"


class View_Article(models.Model):
    """
    View_Article model
    user_id- FK to User model
    article_id- FK to Article model
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)

    @staticmethod
    def amount_of_views_article(article_id):
        """
        Method to return the amount of views of an article
        :param article_id: The article to count the views on
        :return: int, the amount of views
        """
        return View_Article.objects.filter(article_id=article_id).count()

    @staticmethod
    def create_view_article(user_id, article_id, db):
        """
        Method create a new View_Article
        :param user_id: the user that viewed the article
        :param article_id: the article that the user viewed
        :return: the view that created
        """
        view_article = View_Article(user_id=user_id, article_id=article_id)
        view_article.save()
        return view_article
