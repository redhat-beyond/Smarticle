import pytest
from projboard.models.article import Article

SEARCHTITLE = 'search_title'
ARTICLES = 'articles'
COUNT = 'num_articles'
VALUE = 'test'
MESSAGE = 'message'
EMPTY_TITLE_MESSAGE = "please enter a title!"


@pytest.mark.django_db
def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_searchpage(client):
    response = client.get("/search/")
    assert response.status_code == 200
    assert [] == response.context[ARTICLES]
    assert '' == response.context[SEARCHTITLE]
    assert 0 == response.context[COUNT]
    assert '' == response.context[MESSAGE]


@pytest.fixture
@pytest.mark.django_db
def search_by_title():
    articles = Article.search_by_title(VALUE)
    return articles


@pytest.mark.django_db
def test_valued_searchpage_results(client, articles):
    response = client.post('/search/', {'title': VALUE})
    assert response.status_code == 200
    assert response.context[SEARCHTITLE] == VALUE
    for i in response.context[ARTICLES]:
        assert i in articles
    assert response.context[COUNT] == len(articles)
    assert response.context[MESSAGE] == ""


@pytest.mark.django_db
def test_empty_searchpage_results(client):
    response = client.post('/search/', {'title': ''})
    assert response.context[MESSAGE] == EMPTY_TITLE_MESSAGE
