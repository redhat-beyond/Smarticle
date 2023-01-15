import pytest
from projboard.models.article import Article
from projboard.models.subject import Subject
from projboard.models.user import User


SEARCHINPUT = 'search_input'
SEARCHMETHOD = 'search_method'
ARTICLES = 'articles'
COUNT = 'num_articles'
VALUE = 'test'
MESSAGE = 'message'

VALIDTITLE = 'world cup'
INVALIDINPUT = 'INVALID'

VALIDSUBJECT = 'Sport'
INVALIDSUBJECT = 'INVALID'

VALIDUSER = 'User2'
INVALIDUSER = 'INVALID'


EMPTY_TITLE_MESSAGE = "please enter a title!"
MY_ARTICLES = 'my_articles'
WRONG_TITLE_MESSAGE = "Article didn\'t found"
WRONG_SUBJECT_MESSAGE = "Subject Not Valid"
WRONG_USER_MESSAGE = "User Name Not Valid"


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
    assert '' == response.context[SEARCHINPUT]
    assert 'title' == response.context[SEARCHMETHOD]
    assert 0 == response.context[COUNT]
    assert '' == response.context[MESSAGE]


@pytest.fixture
@pytest.mark.django_db
def articles_by_title():
    articles_by_title = Article.search_by_title(VALIDTITLE)
    return articles_by_title


@pytest.fixture
@pytest.mark.django_db
def invalid_articles_by_title():
    invalid_articles_by_title = Article.search_by_title(INVALIDINPUT)
    return invalid_articles_by_title


@pytest.fixture
@pytest.mark.django_db
def articles_by_subject():
    subject = Subject.objects.get(name=VALIDSUBJECT)
    articles_by_subject = Article.search_by_subject(subject.id)
    return articles_by_subject


@pytest.fixture
@pytest.mark.django_db
def articles_by_user():
    user = User.get_user_by_nickname(VALIDUSER)
    valid_articles_by_user = Article.search_by_user(user.id)
    return valid_articles_by_user


@pytest.mark.django_db
def test_valid_title_searchpage_results(client, articles_by_title):
    response = client.post('/search/', {'searchInput': VALIDTITLE, 'searchOptions': 'title'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == VALIDTITLE
    for i in response.context[ARTICLES]:
        assert i in articles_by_title
    assert response.context[COUNT] == len(articles_by_title)
    assert response.context[MESSAGE] == ""


@pytest.mark.django_db
def test_invalid_title_searchpage_results(client, invalid_articles_by_title):
    response = client.post('/search/', {'searchInput': INVALIDINPUT, 'searchOptions': 'title'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == INVALIDINPUT
    for i in response.context[ARTICLES]:
        assert i in invalid_articles_by_title
    assert response.context[COUNT] == len(invalid_articles_by_title)
    assert response.context[MESSAGE] == WRONG_TITLE_MESSAGE


@pytest.mark.django_db
def test_valid_subject_searchpage_results(client, articles_by_subject):
    response = client.post('/search/', {'searchInput': VALIDSUBJECT, 'searchOptions': 'subject'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == VALIDSUBJECT
    for i in response.context[ARTICLES]:
        assert i in articles_by_subject
    assert response.context[COUNT] == len(articles_by_subject)
    assert response.context[MESSAGE] == ""


@pytest.mark.django_db
def test_invalid_subject_searchpage_result(client):
    response = client.post('/search/', {'searchInput': INVALIDSUBJECT, 'searchOptions': 'subject'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == INVALIDSUBJECT
    assert response.context[COUNT] == 0
    assert response.context[MESSAGE] == WRONG_SUBJECT_MESSAGE


@pytest.mark.django_db
def test_valid_user_searchpage_results(client, articles_by_user):
    response = client.post('/search/', {'searchInput': VALIDUSER, 'searchOptions': 'user'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == VALIDUSER
    for i in response.context[ARTICLES]:
        assert i in articles_by_user
    assert response.context[COUNT] == len(articles_by_user)
    assert response.context[MESSAGE] == ""


@pytest.mark.django_db
def test_invalid_user_searchpage_result(client):
    response = client.post('/search/', {'searchInput': INVALIDUSER, 'searchOptions': 'user'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == INVALIDUSER
    assert response.context[COUNT] == 0
    assert response.context[MESSAGE] == WRONG_USER_MESSAGE


@pytest.mark.django_db
def test_empty_searchpage_results(client):
    response = client.post('/search/', {'searchInput': '', 'searchOptions': 'title'})
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
