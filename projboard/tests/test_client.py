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


@pytest.fixture
@pytest.mark.django_db
def User2():
    return User.get_user_by_nickname("User2")


@pytest.mark.django_db
def test_get_searchpage(client, User2):
    response = client.get(f"/search/{User2.nickname}/")
    assert response.status_code == 200
    assert response.context['user'] == User2
    assert [] == response.context[ARTICLES]
    assert '' == response.context[SEARCHINPUT]
    assert 'title' == response.context[SEARCHMETHOD]
    assert 0 == response.context[COUNT]
    assert '' == response.context[MESSAGE]


@pytest.mark.django_db
def test_get_empty_searchpage(client):
    response = client.get("/search/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_invalid_nickname_searchpage(client):
    response = client.get("/search/fakeUser2/")
    assert response.status_code == 404


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
def test_valid_title_searchpage_results(client, articles_by_title, User2):
    response = client.post(f'/search/{User2.nickname}/', {'searchInput': VALIDTITLE, 'searchOptions': 'title'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == VALIDTITLE
    for i in response.context[ARTICLES]:
        assert i in articles_by_title
    assert response.context[COUNT] == len(articles_by_title)
    assert response.context[MESSAGE] == ""


@pytest.mark.django_db
def test_invalid_title_searchpage_results(client, invalid_articles_by_title, User2):
    response = client.post(f'/search/{User2.nickname}/', {'searchInput': INVALIDINPUT, 'searchOptions': 'title'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == INVALIDINPUT
    for i in response.context[ARTICLES]:
        assert i in invalid_articles_by_title
    assert response.context[COUNT] == len(invalid_articles_by_title)
    assert response.context[MESSAGE] == WRONG_TITLE_MESSAGE


@pytest.mark.django_db
def test_valid_subject_searchpage_results(client, articles_by_subject, User2):
    response = client.post(f'/search/{User2.nickname}/', {'searchInput': VALIDSUBJECT, 'searchOptions': 'subject'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == VALIDSUBJECT
    for i in response.context[ARTICLES]:
        assert i in articles_by_subject
    assert response.context[COUNT] == len(articles_by_subject)
    assert response.context[MESSAGE] == ""


@pytest.mark.django_db
def test_invalid_subject_searchpage_result(client, User2):
    response = client.post(f'/search/{User2.nickname}/', {'searchInput': INVALIDSUBJECT, 'searchOptions': 'subject'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == INVALIDSUBJECT
    assert response.context[COUNT] == 0
    assert response.context[MESSAGE] == WRONG_SUBJECT_MESSAGE


@pytest.mark.django_db
def test_valid_user_searchpage_results(client, articles_by_user, User2):
    response = client.post(f'/search/{User2.nickname}/', {'searchInput': VALIDUSER, 'searchOptions': 'user'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == VALIDUSER
    for i in response.context[ARTICLES]:
        assert i in articles_by_user
    assert response.context[COUNT] == len(articles_by_user)
    assert response.context[MESSAGE] == ""


@pytest.mark.django_db
def test_invalid_user_searchpage_result(client, User2):
    response = client.post(f'/search/{User2.nickname}/', {'searchInput': INVALIDUSER, 'searchOptions': 'user'})
    assert response.status_code == 200
    assert response.context[SEARCHINPUT] == INVALIDUSER
    assert response.context[COUNT] == 0
    assert response.context[MESSAGE] == WRONG_USER_MESSAGE


@pytest.mark.django_db
def test_empty_searchpage_results(client, User2):
    response = client.post(f'/search/{User2.nickname}/', {'searchInput': '', 'searchOptions': 'title'})
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
    assert response.status_code == 302


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


def test_signup_page(client):
    response = client.get("/signup/")
    assert response.status_code == 200
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert 'signup/signup.html' in template_names


@pytest.mark.django_db
def test_read_view_new_article(client, world_cup_article, User2):
    """
    Testing the number of views in a new article (not viewed yet)
    => num of views should increase by 1
    """
    # recieving world cup article that User 2 didn't view yet, plus getting num views of it
    num_views1 = world_cup_article.num_of_views

    # preparing the page route
    route = '/article/{0}/{1}/'.format(User2.nickname, world_cup_article.id)

    # Send a GET request to the page
    response = client.get(route)

    assert response.status_code == 200
    assert response.context['user'] == User2
    # Create a set of template names from the templates used in the response
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    # And check if that show/read_article.html is in the set.
    assert 'show/read_article.html' in template_names
    # checking the result of the view return
    assert response.context['article'] == world_cup_article
    # getting num of views after viewing the article
    num_views2 = response.context['article'].num_of_views
    # checking that num views has been increased
    assert num_views2 == num_views1 + 1


@pytest.mark.django_db
def test_like_article(client, world_cup_article, User2):
    # recieving world cup article that User 2 didn't like yet, plus getting num likes of it
    num_likes1 = world_cup_article.num_of_likes

    # preparing the page route
    route = '/article/{0}/{1}/'.format(User2.nickname, world_cup_article.id)
    # Send a POST request to the page
    response = client.post(route, {'like_method': 'Add'})

    assert response.status_code == 200
    assert response.context['article'] == world_cup_article
    # getting num of likes after liking the article
    num_likes2 = response.context['article'].num_of_likes
    #  checking that num likes has been increased
    assert num_likes2 == num_likes1 + 1


@pytest.mark.django_db
def test_unlike_article(client, math_article, User2):
    # recieving world cup article that User 2 didn't like yet, plus getting num likes of it
    num_likes1 = math_article.num_of_likes

    # preparing the page route
    route = '/article/{0}/{1}/'.format(User2.nickname, math_article.id)
    # Send a POST request to the page
    response = client.post(route, {'like_method': 'Remove'})

    assert response.status_code == 200
    assert response.context['article'] == math_article
    # getting num of likes after liking the article
    num_likes2 = response.context['article'].num_of_likes
    # checking that num likes has been dicreased
    assert num_likes2 == num_likes1 - 1


@pytest.mark.django_db
def test_read_already_viewed_article(client, math_article, User2):
    """
    Testing the number of views in an already viewed article (got viewed in the past)
    => num of views should't increase
    """
    # recieving world cup article that User 2 didn't view yet, plus getting num views of it
    num_views1 = math_article.num_of_views

    # preparing the page route
    route = '/article/{0}/{1}/'.format(User2.nickname, math_article.id)

    # Send a GET request to the page
    response = client.get(route)

    assert response.status_code == 200
    assert response.context['user'] == User2
    # Create a set of template names from the templates used in the response
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    # And check if that show/read_article.html is in the set.
    assert 'show/read_article.html' in template_names

    # checking the result of the view return
    assert response.context['article'] == math_article
    # getting num of views after viewing the article
    num_views2 = response.context['article'].num_of_views
    #  checking that num views didn't increased
    assert num_views2 == num_views1
