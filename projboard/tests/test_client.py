import pytest
from projboard.models.article import Article
from projboard.forms import EditArticleForm

SEARCHTITLE = 'search_title'
ARTICLES = 'articles'
COUNT = 'num_articles'
VALUE = 'test'
MESSAGE = 'message'
EMPTY_TITLE_MESSAGE = "please enter a title!"
MY_ARTICLES = 'my_articles'
INVALID_ARTICLE = 1234567
VALID_TITLE = 'valid title'
VALID_SUBJECT = 5
VALID_CONTENT = 'valid content'
NEW_TITLE = 'new title'
NEW_SUBJECT = 4
NEW_CONTENT = 'new content'


@pytest.mark.django_db
def test_homepage(client, articles_num):
    response = client.get("/")
    assert response.status_code == 200
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    # CHECK IF THE ARTICLES CONTAINTS THE CORRECT NUMBER OF ARTICLES
    assert len(response.context['articles']) == articles_num
    assert 'landing/homepage.html' in template_names


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


@pytest.mark.django_db
def test_get_my_articles(client, user, user_articles):
    # test a correct nickname
    response = client.get(f"/my_articles/{user.nickname}/")
    assert response.status_code == 200

    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert 'myArticles/my_articles.html' in template_names

    # test that all the users article found by length and by articles
    assert response.context[COUNT] == len(user_articles)
    for article in response.context[MY_ARTICLES]:
        assert article in user_articles


@pytest.mark.django_db
def test_my_articles_empty_nickname(client):
    # test edge case of sending user nickname = ''
    response = client.get("/my_articles/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_my_articles_invalid_nickname(client, user):
    # test edge case of sending nickname that doesnt belong to any user in DB
    response = client.get(f"/my_articles/fake{user.nickname}/")
    assert response.status_code == 404


def test_error_404(client):
    response = client.delete('/NOT_EXSITS_FAKE_ROUTE/')

    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert '404.html' in template_names
    assert response.status_code == 404


def test_aboutpage(client):
    # Send a GET request to the page
    response = client.get("/about/")
    # Verify that the response status code is 200 (indicating a successful request)
    assert response.status_code == 200
    # Create a set of template names from the templates used in the response
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    # And check if that 'about/about.html' is in the set.
    assert 'about/about.html' in template_names


@pytest.mark.django_db
def test_delete_article(client, article):
    # Test article in DB
    assert article in set(Article.objects.all())

    # Test deletion response
    response = client.get(f"/delete_article/{article.id}/")
    assert response.status_code == 302

    # Test article deletion
    assert article not in set(Article.objects.all())


@pytest.mark.django_db
def test_fail_delete_article(client):
    response = client.get(f"/delete_article/{INVALID_ARTICLE}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_edit_article(client, article):
    # test the article before edit
    assert article.title != NEW_TITLE

    # test article editing
    data = {"title": NEW_TITLE, "subject_id": NEW_SUBJECT, "content": NEW_CONTENT}
    response = client.post(f"/edit_article/{article.id}/", data=data)
    assert response.status_code == 302
    assert response.url == f"/my_articles/{article.user_id.nickname}/"

    edited_article = Article.objects.get(pk=article.id)
    assert edited_article.title == NEW_TITLE
    assert edited_article.subject_id.id == NEW_SUBJECT
    assert edited_article.content == NEW_CONTENT


@pytest.mark.django_db
def test_edit_invalid_article(client):
    response = client.get(f"/edit_article/{INVALID_ARTICLE}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_edit_article_form():
    form_data = {
        'title': VALID_TITLE,
        'subject': VALID_SUBJECT,
        'content': VALID_CONTENT
    }
    form = EditArticleForm(data=form_data)
    assert form.is_valid
