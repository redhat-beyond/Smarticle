import pytest
from projboard.models.user import User


NAME = "RAWAD"
NICKNAME = "R1998"
EMAIL = "rawad@gmail.com"
PASSWORD = "rawad!@#"


@pytest.fixture
def generate_user():
    user = User(name=NAME, nickname=NICKNAME, email=EMAIL, password=PASSWORD)
    user.save()
    return user


class TestUserModel:
    @pytest.mark.django_db()
    def test_new_user(self, generate_user):
        user = User.get_user(generate_user.email, generate_user.nickname, generate_user.name, generate_user.nickname)
        assert generate_user.name == user.name
        assert generate_user.nickname == user.nickname
        assert generate_user.email == user.email
        assert generate_user.password == user.password

    @pytest.mark.django_db()
    def test_create_user(self, generate_user):
        assert generate_user in User.objects.all()

    @pytest.mark.django_db()
    def test_delete_user(self, generate_user):
        # Delete user by nickname
        generate_user.delete_user(generate_user.nickname)
        assert generate_user not in User.objects.all()

    @pytest.mark.django_db()
    def test_get_user(self, generate_user):
        # Get user by nickname
        assert User.get_user_by_nickname(generate_user.nickname) in User.objects.all()
