import pytest
from projboard.models.user import User


NAME = "RAWAD"
NICKNAME = "USER3"
EMAIL = "rawad@gmail.com"
PASSWORD = "123456"
# NICKNAME FAIL FOR FAIL TESTS
NICKNAME_FAIL = "undefined_user"


class TestUserModel:

    @pytest.fixture
    def fake_user(self):
        user = User(email=EMAIL, password=PASSWORD, name=NAME, nickname=NICKNAME_FAIL)
        return user

    @pytest.fixture
    def generate_user(self):
        user = User(email=EMAIL, password=PASSWORD, name=NAME, nickname=NICKNAME)
        user.save()
        return user

    @pytest.mark.django_db
    def test_generate_user(self, generate_user):
        # Test generarting new user in DB
        assert generate_user in User.objects.all()

    @pytest.mark.django_db
    def test_create_user(self):
        # Testing if generate_user
        user = User.create_user(EMAIL, PASSWORD, NAME, NICKNAME)
        assert user in User.objects.all()

    @pytest.mark.django_db
    def test_get_user_by_nickname(self, generate_user):
        # Tests that the user is in the DB
        user = User.get_user_by_nickname(NICKNAME)
        assert generate_user.name == user.name
        assert generate_user.nickname == user.nickname
        assert generate_user.email == user.email
        assert generate_user.password == user.password

    @pytest.mark.django_db
    def test_get_user_by_nickname_fail(self, fake_user):
        # Tests that the user is not in the DB
        user = User.get_user_by_nickname(fake_user.nickname)
        assert user not in User.objects.all()

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_delete_user_by_nickname(self, generate_user):
        # Delete user by nickname
        generate_user.delete_user_by_nickname(generate_user.nickname)
        assert generate_user not in User.objects.all()

    @pytest.mark.django_db
    def test_delete_user_by_nickname_fail(self, fake_user):
        # Delete user by nickname fail
        assert fake_user.delete_user_by_nickname(fake_user.nickname) is False
