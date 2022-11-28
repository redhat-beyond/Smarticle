from django.db import models
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

    @staticmethod
    def get_user(email, password, name, nickname):
        """
         Method to create a new user,
         but also checks if user is already exists
         [get user either by mail or by nickname]
        :param email: user's email
        :param password: user's password
        :param name: user's name
        :param nickname: user's nickname
        :return: new user
        """
        try:
            user = User.objects.get(nickname=nickname)
            # user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            user = User(email=email, password=password, name=name, nickname=nickname)
            user.save()
            return user

    @staticmethod
    def delete_user(nickname):
        """
         Method to delete a user
        :param nickname: nickname to get the user
        :return:  TRUE/FALSE if the user deleted/not
        """
        try:
            user = User.objects.get(nickname=nickname)
            user.delete()
        except User.DoesNotExist:
            return False
        return True

    @staticmethod
    def get_user_articles_by_likes(nickname):
        """
        Method get nickname and return User object if exist, otherwise None
        :param nickname: the nickname to search
        :return: User object
        """
        # NOT FINISHED YET
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return None
        return user

    @staticmethod
    def get_user_articles_by_views(nickname):
        """
        Method get nickname and return User object if exist, otherwise None
        :param nickname: the nickname to search
        :return: User object
        """
        # NOT FINISHED YET
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return None
        return user
