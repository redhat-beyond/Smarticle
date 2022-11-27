import pytest
from projboard.models import Like, User, Article, Subject

U = ['usertest@gmail.co.il', '123456', 'John Doe', 'USER_TEST']
USER_TEST = User(email=U[0], password=U[1], name=U[2], nickname=U[3])

SUBJECT_TEST = Subject(name='Test')
A = [USER_TEST, 'World cup', SUBJECT_TEST, 'Messi is better then CR7']
ARTICLE_TEST = Article(user_id=A[0], title=A[1], subject_id=A[2], content=A[3])


@pytest.fixture
def generate_like():
    SUBJECT_TEST.save()
    USER_TEST.save()
    ARTICLE_TEST.save()
    Like(user_id=USER_TEST, article_id=ARTICLE_TEST).save()
    return USER_TEST, ARTICLE_TEST


@pytest.mark.django_db
class TestLikeModel:
    def test_create_like(self):
        USER_TEST.save()
        SUBJECT_TEST.save()
        ARTICLE_TEST.save()
        like = Like.create_like(USER_TEST, ARTICLE_TEST)

        assert like.user_id.name == USER_TEST.name
        assert like.article_id.title == ARTICLE_TEST.title

    def test_delete_like(self):
        USER_TEST.save()
        SUBJECT_TEST.save()
        ARTICLE_TEST.save()

        result = Like.delete_like(USER_TEST, ARTICLE_TEST)
        assert not result

        like = Like.create_like(USER_TEST, ARTICLE_TEST)
        result = Like.delete_like(like.user_id, like.article_id)
        assert result

    def test_amount_of_likes_article_1(self, generate_like):
        amount_likes = Like.amount_of_likes_article(generate_like[1])
        assert amount_likes == 1

    def test_amount_of_likes_article_0(self):
        amount_likes = Like.amount_of_likes_article(ARTICLE_TEST)
        assert amount_likes == 0
