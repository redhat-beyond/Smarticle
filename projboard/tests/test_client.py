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


@pytest.mark.django_db
def test_create_article_get(client):
    response = client.get('/create_article/')
    assert response.status_code == 200

    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert 'article/article.html' in template_names


@pytest.mark.django_db
def test_fill_article_post(client, article, django_capture_on_commit_callbacks):
    response = client.get('/create_article/')
    assert response.status_code == 200

    # Page before the post
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert 'article/article.html' in template_names

    with django_capture_on_commit_callbacks(execute=True):
        response = client.post(
            '/create_article/', {
                'title': article.title + ' form',
                'subject_id': 1,
                'user_id': 1,
                'content': article.content
            })

    # Page after the post
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    # TODO change board.html to my_article.html
    assert 'landing/homepage.html' in template_names
    assert response.status_code == 200


@pytest.mark.django_db
def test_fill_article_delete(client):
    response = client.delete('/create_article/')
    assert response.status_code == 404

    # Page before the post
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert '404.html' in template_names


def test_error_404(client):
    response = client.delete('/NOT_EXSITS_FAKE_ROUTE/')

    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert '404.html' in template_names
    assert response.status_code == 404
