import pytest
from projboard.forms import NewUserForm
from projboard.models.user import User
from conftest import (
                    VALID_USER,
                    VALID_EMAIL,
                    VALID_PASSWORD,
                    INVALID_EMAIL,
                    INVALID_PASSWORD_MISMATCH,
                    MISMATCH_MESSAGE_ERROR,
                    VALID_NAME,
                    SIGNUP_PATH
                    )


@pytest.mark.django_db
def test_valid_form():
    form_data = {
        'email': VALID_EMAIL,
        'name': VALID_NAME,
        'nickname': VALID_USER,
        'password': VALID_PASSWORD,
        'password_confirm': VALID_PASSWORD,
    }
    form = NewUserForm(data=form_data)
    if form.is_valid():
        assert True
    else:
        assert False


@pytest.mark.django_db
def test_invalid_form():
    form_data = {
        'email': INVALID_EMAIL,
        'name': VALID_NAME,
        'nickname': VALID_USER,
        'password': VALID_PASSWORD,
        'password_confirm': VALID_PASSWORD,
    }
    form = NewUserForm(data=form_data)
    if form.is_valid():
        assert False
    else:
        assert True


@pytest.mark.django_db
def test_valid_registration(client):
    valid_data = {
        'email': VALID_EMAIL,
        'name': VALID_NAME,
        'nickname': VALID_USER,
        'password': VALID_PASSWORD,
        'password_confirm': VALID_PASSWORD,
        }
    response = client.post(SIGNUP_PATH, data=valid_data)
    # ASSERTION TO SHOW THAT SIGNUP SWITCHED TO HOMEPAGE (LOGIN PAGE LATER)
    assert response.status_code == 302
    assert User.get_user_by_nickname(VALID_USER)
    # THIS ASSERT IS SETTED FOR HOMEPAGE BECAUSE /LOGIN ARENT READY YET
    assert response.url == '/'
# STILL NEED TO ADD MORE TESTS


@pytest.mark.django_db
def test_invalid_email_registration(client):
    invalid_data = {
        'email': INVALID_EMAIL,
        'name': VALID_NAME,
        'nickname': VALID_USER,
        'password': VALID_PASSWORD,
        'password_confirm': VALID_PASSWORD,
        }
    response = client.post(SIGNUP_PATH, data=invalid_data)
    assert response.status_code == 200
    assert response.request['PATH_INFO'] == SIGNUP_PATH


@pytest.mark.django_db
def test_invalid_password_registration(client):
    invalid_data = {
        'email': VALID_EMAIL,
        'name': VALID_NAME,
        'nickname': VALID_USER,
        'password': VALID_PASSWORD,
        'password_confirm': INVALID_PASSWORD_MISMATCH,
        }
    response = client.post(SIGNUP_PATH, data=invalid_data)
    assert response.status_code == 200
    # assert response.context['form'].error_message == MISMATCH_MESSAGE_ERROR
    messages = list(response.context['messages'])
    assert len(messages) == 1
    assert str(messages[0]) == MISMATCH_MESSAGE_ERROR
