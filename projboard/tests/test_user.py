import pytest
from projboard.models import User


@pytest.fixture
def generate_user(email='user@gmail.com', password='password', name='name', nickname='nickname'):
    user = User(email=email, password=password, name=name, nickname=nickname)
    user.save()
    return user


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self, generate_user):
        user = User.get_user_by_nickname('nickname')
        assert user.email == generate_user.email
        assert user.password == generate_user.password
        assert user.name == generate_user.name
        assert user.nickname == generate_user.nickname

    def test_delete_user(self, generate_user):
        assert User.delete_user(generate_user)
        user = User.get_user_by_nickname('nickname')
        assert not user

    def test_get_user(self, generate_user):
        assert User.get_user_by_nickname('nickname') == generate_user
