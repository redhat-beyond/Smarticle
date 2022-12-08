from django.db import models


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
        user = User.objects.get(nickname=nickname)
        if user not in User.objects.all():
            raise User.DoesNotExist
        else:
            return user

    @staticmethod
    def create_user(email, password, name, nickname):
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
        user = User(email=email, password=password, name=name, nickname=nickname)
        # user = User.objects.get(email=email)
        user.save()
        return user

    @staticmethod
    def delete_user_by_nickname(nickname):
        """
         Method to delete a user by his nickname
        :param nickname: nickname to get the user
        :return:  TRUE/FALSE if the user deleted/not
        """
        user = User.get_user_by_nickname(nickname=nickname)
        if user not in User.objects.all():
            raise User.DoesNotExist
        else:
            user.delete()
