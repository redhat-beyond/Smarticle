import pytest
from projboard.models.article import Article, User, View_Article, Like, Subject


TITLE = "Article Test"
CONTENT = "I'm not gonna write all that!"


@pytest.fixture
def subjects():
    subject_1 = Subject(name='N')
    subject_2 = Subject(name='R')
    subject_1.save()
    subject_2.save()
    return [subject_1, subject_2]


@pytest.fixture
def users():
    user = User(name="my_username", nickname="my_nickname", email="my_email@gmail.com", password="my_password")
    user1 = User(name="John", nickname="J99", email="John@gmail.com", password="John123")
    user.save()
    user1.save()
    return [user, user1]


@pytest.fixture
def articles(users, subjects):
    articles_list = []
    for i in range(len(users)):
        article = Article(user_id=users[i], title=TITLE, content=CONTENT, subject_id=subjects[i])
        article.save()
        articles_list.append(article)

    return articles_list


@pytest.fixture
def like(users, articles):
    like = Like(user_id=users[0], article_id=articles[0])
    like.save()
    return like


@pytest.fixture
def view(users, articles):
    view_article = View_Article(user_id=users[0], article_id=articles[0])
    view_article.save()
    return view_article
