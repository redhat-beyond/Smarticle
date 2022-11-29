import pytest
from projboard.models import Like, User, Article, Subject


TITLE = "Article Test"
CONTENT = "I'm not gonna write all that!"
NAME = "Shalev"


@pytest.mark.django_db
class TestLikeModel:

    @pytest.fixture
    @pytest.mark.django_db
    def create_subjects(self):
        sup = Subject(name='N')
        sup1 = Subject(name='R')
        sup.save()
        sup1.save()
        return [sup, sup1]

    @pytest.fixture
    @pytest.mark.django_db
    def create_user(self):
        user = User(name=NAME, nickname="S99", email="Shalev@gmail.com", password="Shalev123")
        user1 = User(name="John", nickname="J99", email="John@gmail.com", password="John123")
        user.save()
        user1.save()
        return [user, user1]

    @pytest.fixture
    @pytest.mark.django_db
    def create_articles(self, create_user, create_subjects):
        articles_list = []
        for i in range(len(create_user)):
            article = Article(user_id=create_user[i], title=TITLE,
                              content=CONTENT, subject_id=create_subjects[i])
            article.save()
            articles_list.append(article)

        return articles_list

    @pytest.fixture
    @pytest.mark.django_db
    def create_like(self, create_user, create_articles):
        like = Like(user_id=create_user[0], article_id=create_articles[0])
        like.save()
        return like

    def test_create_like(self, create_like):
        assert create_like.user_id.name == NAME
        assert create_like.article_id.title == TITLE

    def test_delete_like(self, create_user, create_like):
        result = Like.delete_like(create_user[1], create_like.article_id)
        assert not result

        result = Like.delete_like(create_like.user_id, create_like.article_id)
        assert result

    @pytest.mark.django_db
    def test_amount_of_likes_article(self, create_like):
        amount_likes = Like.amount_of_likes_article(create_like.article_id)
        assert len(Like.objects.filter(article_id=create_like.article_id)) == amount_likes

        Like.delete_like(create_like.user_id, create_like.article_id)
        assert len(Like.objects.filter(article_id=create_like.article_id)) != amount_likes
