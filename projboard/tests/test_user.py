import pytest
from projboard.models.user import User
NAME = "my_username"
NICKNAME = "my_nickname"
EMAIL = "my_email@gmail.com"
PASSWORD = "my_password"
NOT_EXISTED_USER = "undefined_user"


@pytest.mark.django_db
class TestUserModel:

    def test_create_users(self, users):
        # Test generarting new user in DB
        assert users[0] in User.objects.all()
        assert users[1] in User.objects.all()

    def test_create_user(self):
        # Testing if generate_user
        user = User.create_user(EMAIL, PASSWORD, NAME, NICKNAME)
        assert user in User.objects.all()

    def test_get_user_by_nickname(self, users):
        # Tests that the user is in the DB
        user = User.get_user_by_nickname(NICKNAME)
        assert users[0].name == user.name
        assert users[0].nickname == user.nickname
        assert users[0].email == user.email
        assert users[0].password == user.password

    def test_get_not_existed_user_by_nickname(self):
        with pytest.raises(User.DoesNotExist, match="User matching query does not exist."):
            assert User.get_user_by_nickname(NOT_EXISTED_USER)

    def test_delete_user_by_nickname(self, users):
        # Delete user by nickname
        users[0].delete_user_by_nickname(users[0].nickname)
        assert users not in User.objects.all()

    def test_delete_not_existed_user_by_nickname(self):
        # Delete not existed user
        with pytest.raises(User.DoesNotExist, match="User matching query does not exist."):
            assert User.delete_user_by_nickname(NOT_EXISTED_USER)
