import pytest
from projboard.models.user import User
NICKNAME = "my_nickname"
NOT_EXISTED_USER = "undefined_user"


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self, user):
        # Test generarting new user in DB
        assert user in User.objects.all()

    def test_create_users(self, users):
        # Test generarting users in DB
        for i in range(len(users)):
            assert users[i] in User.objects.all()

    def test_get_user_by_nickname(self, user):
        # Tests that the user we get from get_user_by_nickname is the same we generated
        get_user = User.get_user_by_nickname(NICKNAME)
        assert user.name == get_user.name
        assert user.nickname == get_user.nickname
        assert user.email == get_user.email
        assert user.password == get_user.password

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
