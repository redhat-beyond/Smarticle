import pytest
from projboard.models.user import User


NAME = "RAWAD"
NICKNAME = "USER3"
EMAIL = "rawad@gmail.com"
PASSWORD = "123456"

# NAME1 = "RAWAD2"
# NICKNAME1 = "USER32"
# EMAIL1 = "rawad2@gmail.com"
# PASSWORD1 = "1234562"


class TestUserModel:

    @pytest.fixture
    @pytest.mark.django_db
    def generate_user(self):
        user = User(email=EMAIL, password=PASSWORD, name=NAME, nickname=NICKNAME)
        user.save()
        return user

    @pytest.mark.django_db
    def test_new_user(self, generate_user):
        user = User.get_user_by_nickname(generate_user.nickname)
        assert generate_user.email == user.email
        assert generate_user.name == user.name
        assert generate_user.nickname == user.nickname
        assert generate_user.password == user.password

    @pytest.mark.django_db
    def test_create_user(self, generate_user):
        assert generate_user in User.objects.all()

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_delete_user(self, generate_user):
        # Delete user by nickname
        generate_user.delete_user(generate_user.nickname)
        assert generate_user not in User.objects.all()

    @pytest.mark.django_db
    def test_get_user(self, generate_user):
        # Get user by nickname
        assert User.get_user_by_nickname(generate_user.nickname) in User.objects.all()
