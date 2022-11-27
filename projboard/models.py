from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


class Subject(models.Model):
    """
    Subject model

    name- A string, the subject name
    """
    name = models.CharField(max_length=100)

    @staticmethod
    def get_subject_by_name(name):
        """
        Method get subject name and return Subject object if exist, otherwise None
        :param name: the name to search
        :return: Subject object
        """
        try:
            subject = User.objects.get(name=name)
        except ObjectDoesNotExist:
            return None
        return subject


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

    @staticmethod
    def get_user_by_nickname(nickname):
        """
        Method get nickname and return User object if exist, otherwise None
        :param nickname: the nickname to search
        :return: User object
        """
        try:
            user = User.objects.get(nickname=nickname)
        except ObjectDoesNotExist:
            return None
        return user


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


class View(models.Model):
    """
    View model

    user_id- FK to User model
    article_id- FK to Article model
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
