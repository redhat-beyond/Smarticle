import pytest


@pytest.mark.django_db
def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_article(client):
    response = client.get('/create_article/')
    assert response.status_code == 200
