import pytest
from projboard.forms import UserForm, CustomUserForm
from conftest import (
                    VALID_USER,
                    VALID_EMAIL,
                    VALID_PASSWORD,
                    INVALID_EMAIL,
                    INVALID_PASSWORD_MISMATCH,
                    VALID_NAME,
                    VALID_NICKNAME,
                    )


@pytest.mark.django_db
def test_valid_form_custom_user():
    form_data = {
        'name': VALID_NAME,
        'nickname': VALID_NICKNAME
    }
    form = CustomUserForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_valid_form():
    form_data = {
        'username': VALID_USER,
        'password': VALID_PASSWORD,
        'email': VALID_EMAIL
    }
    form = UserForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_form():
    form_data = {
        'username': VALID_USER,
        'password': VALID_PASSWORD,
        'email': INVALID_EMAIL
    }
    form = UserForm(data=form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_valid_login(client):
    response = client.post('/login/', data={'username': 'User1', 'password': '123456'})
    assert response.status_code == 302
    assert response.url == '/'


@pytest.mark.django_db
def test_invalid_login(client):
    response = client.post('/login/', data={'username': VALID_USER, 'password': INVALID_PASSWORD_MISMATCH})
    assert response.status_code == 200
    assert response.request['PATH_INFO'] == '/login/'
