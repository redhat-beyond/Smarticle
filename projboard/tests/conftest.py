import pytest
from projboard.models.article import Article, User, View_Article, Like, Subject

TITLE = "Article Test"
CONTENT = "I'm not gonna write all that!"
VALID_USER = "smarticleUser"
VALID_EMAIL = "user@telhai.ac.il"
VALID_NAME = "smarticleName"
VALID_PASSWORD = "smarticlePassword"
INVALID_EMAIL = "user.telhai.ac.il"
INVALID_PASSWORD_MISMATCH = "smarticlePasswordMismatch"
LOGIN_PATH = "login/login.html"
SIGNUP_PATH = "/signup/"
MISMATCH_MESSAGE_ERROR = "Unsuccessful registration. Invalid information."
VALID_DATA = {
    'email': 'example@example.com',
    'name': 'John Doe',
    'nickname': 'johndoe',
    'password': 'password',
    'password_confirm': 'password',
}


@pytest.fixture
@pytest.mark.django_db
def user():
    user = User(name="my_username", nickname="my_nickname", email="my_email@gmail.com", password="my_password")
    user.save()
    return user


@pytest.fixture
@pytest.mark.django_db
def users(user):
    new_user = User(name="John", nickname="J99", email="John@gmail.com", password="John123")
    new_user.save()
    return [user, new_user]


@pytest.fixture
@pytest.mark.django_db
def subject():
    subject = Subject.create_and_get_subject(name="yael")
    subject.save()
    return subject


@pytest.fixture
@pytest.mark.django_db
def subjects(subject):
    new_subject = Subject.create_and_get_subject(name="gal")
    new_subject.save()
    return [subject, new_subject]


@pytest.fixture
@pytest.mark.django_db
def article(user, subject):
    article = Article(user_id=user, title=TITLE, content=CONTENT, subject_id=subject)
    article.save()
    return article


@pytest.fixture
@pytest.mark.django_db
def articles(users, subjects):
    articles_list = []
    for i in range(len(users)):
        article = Article(user_id=users[i], title=TITLE, content=CONTENT, subject_id=subjects[i])
        article.save()
        articles_list.append(article)

    return articles_list


@pytest.fixture
@pytest.mark.django_db
# Test user's like on article
def like(user, article):
    like = Like(user_id=user, article_id=article)
    like.save()
    return like


@pytest.fixture
@pytest.mark.django_db
# Test user's view on article
def view(user, article):
    view_article = View_Article(user_id=user, article_id=article)
    view_article.save()
    return view_article


@pytest.fixture
@pytest.mark.django_db
def articles_num():
    articles_num = Article.objects.count()
    return articles_num


@pytest.fixture
@pytest.mark.django_db
def user_articles(user):
    user_articles = Article.search_by_user(user)
    return user_articles


@pytest.fixture
@pytest.mark.django_db
def world_cup_article():
    return Article.search_by_title('world cup')[0]


@pytest.fixture
@pytest.mark.django_db
def math_article():
    return Article.search_by_title('1+1')[0]
