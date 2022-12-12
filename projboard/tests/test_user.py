import pytest
from projboard.models.user import User
NAME = "my_username"
NICKNAME = "my_nickname"
EMAIL = "my_email@gmail.com"
PASSWORD = "my_password"
NOT_EXISTED_USER = "undefined_user"


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self, user):
        # Test generarting new user in DB
        assert user in User.objects.all()

    def test_create_users(self, users):
        # Test generarting users in DB
        assert users[0] in User.objects.all()
        assert users[1] in User.objects.all()

    def test_get_user_by_nickname(self, user):
        # Tests that the user is in the DB
        user = User.get_user_by_nickname(NICKNAME)
        assert user.name == user.name
        assert user.nickname == user.nickname
        assert user.email == user.email
        assert user.password == user.password

    def test_get_not_existed_user_by_nickname(self):
        with pytest.raises(User.DoesNotExist, match="User matching query does not exist."):
            assert User.get_user_by_nickname(NOT_EXISTED_USER)

    def test_delete_user_by_nickname(self, user):
        # Delete user by nickname
        user.delete_user_by_nickname(user.nickname)
        assert user not in User.objects.all()

    def test_delete_not_existed_user_by_nickname(self):
        # Delete not existed user
        with pytest.raises(User.DoesNotExist, match="User matching query does not exist."):
            assert User.delete_user_by_nickname(NOT_EXISTED_USER)
