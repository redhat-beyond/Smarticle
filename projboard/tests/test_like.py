import pytest
from projboard.models import Like, User, Article, Subject

USER_DETAILS = ['usertest@gmail.co.il', '123456', 'John Doe', 'USER_TEST']
USER_TEST = User(email=USER_DETAILS[0], password=USER_DETAILS[1], name=USER_DETAILS[2], nickname=USER_DETAILS[3])

SUBJECT_TEST = Subject(name='Test')
ARTICLE_DETAILS = [USER_TEST, 'World cup', SUBJECT_TEST, 'Messi is better then CR7']
ARTICLE_TEST = Article(user_id=ARTICLE_DETAILS[0], title=ARTICLE_DETAILS[1],
                       subject_id=ARTICLE_DETAILS[2], content=ARTICLE_DETAILS[3])


@pytest.fixture
def generate_like(db, create_user, create_subject, create_article):
    Like(user_id=create_user, article_id=create_article).save()
    return create_user, create_article


@pytest.fixture
def create_user(db):
    USER_TEST.save()
    return USER_TEST


@pytest.fixture
def create_subject(db):
    SUBJECT_TEST.save()
    return SUBJECT_TEST


@pytest.fixture
def create_article(db):
    ARTICLE_TEST.save()
    return ARTICLE_TEST


@pytest.mark.django_db
class TestLikeModel:
    def test_create_like(self, create_user, create_subject, create_article):
        like = Like.create_like(create_user, create_article)
        assert like.user_id.name == USER_TEST.name
        assert like.article_id.title == ARTICLE_TEST.title

    def test_delete_like(self, create_user, create_subject, create_article):
        result = Like.delete_like(create_user, create_article)
        assert not result

        like = Like.create_like(create_user, create_article)
        result = Like.delete_like(like.user_id, like.article_id)
        assert result

    def test_amount_of_likes_article_1(self, generate_like):
        amount_likes = Like.amount_of_likes_article(generate_like[1])
        assert len(Like.objects.filter(article_id=ARTICLE_TEST)) == amount_likes

    def test_amount_of_likes_article_0(self):
        amount_likes = Like.amount_of_likes_article(ARTICLE_TEST)
        assert len(Like.objects.filter(article_id=ARTICLE_TEST)) == amount_likes
