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
            subject = Subject.objects.get(name=name)
        except ObjectDoesNotExist:
            return None
        return subject

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def get_list_subjects_names():
        """
        Method get list subject names
        :return: the list of subject
        """
        subjects_list = list(Subject.objects.all().values_list('name', flat=True))
        return subjects_list

    @staticmethod
    def create_and_get_subject(name):
        """
        Method create a new subject
        :param name: The name of the subject
        :return: the subject that created
        """
        try:
            subject = Subject.objects.get(name=name)
            return subject
        except Subject.DoesNotExist:
            subject = Subject(name=name)
            subject.save()
            return subject

    @staticmethod
    def rename_subject(existing_name, new_name):
        """
        Method rename the subject name
        :param existing_name: The name of the existing subject
        :param new_name: The new name of the subject
        :return: The new name of the subject
        """
        try:
            subject = Subject.objects.get(name=existing_name)
            subject.name = new_name
            subject.save()
            return subject
        except Subject.DoesNotExist:
            return None

    @staticmethod
    def delete_subject(name):
        """
        Method delete a subject
        :param name: The name of the subject
        :return: True if success
        """
        try:
            subject = Subject.objects.get(name=name)
            subject.delete()
            return True
        except Subject.DoesNotExist:
            return False


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


class View(models.Model):
    """
    View model

    user_id- FK to User model
    article_id- FK to Article model
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
