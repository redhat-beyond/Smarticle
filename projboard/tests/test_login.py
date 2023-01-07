import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed

VALID_USER = "smarticleUser"
VALID_EMAIL = "user@telhai.ac.il"
VALID_PASSWORD = "smarticlePassword"

INVALID_EMAIL = "user.telhai.ac.il"
INVALID_PASSWORD_MISMATCH = "smarticlePasswordMismatch"
LOGIN_PATH = "login/login.html"


@pytest.mark.django_db
class TestLogin:
    @pytest.fixture
    def registered_user(self):
        user = User.objects.create_user(username=VALID_USER, email=VALID_EMAIL, password=VALID_PASSWORD)
        user.save()

    def test_login(self, client):
        response = client.get('/login/')
        assert response.status_code == 200
        assertTemplateUsed(response, LOGIN_PATH)

    def test_valid_login(self, client, registered_user):
        response = client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        assert response.status_code == 302
        assert response.url == '/'

    def test_invalid_login(self, client, registered_user):
        response = client.post('/login/', data={'username': VALID_USER, 'password': INVALID_PASSWORD_MISMATCH})
        assert response.status_code == 200
        assert response.request['PATH_INFO'] == '/login/'
