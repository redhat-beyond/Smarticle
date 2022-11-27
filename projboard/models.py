from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist



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
    SUBJECTS = [
            ('N', 'Nature'),
            ('B', 'Business'),
            ('T', 'Technology'),
            ('E', 'Economie'),
            ('I', 'Industry'),
            ('P', 'Policy'),        
            ('SC', 'Science'),
            ('SP', 'Sport'),
            ('LS', 'Life Style'),
            ('O', 'Other'),
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    subject = models.CharField(default= 'O', blank = True, max_length=100, choices=SUBJECTS)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class View(models.Model):
    """
    View model

    user_id- FK to User model
    article_id- FK to Article model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
