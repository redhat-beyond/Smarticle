import pytest
from projboard.models.user import User
from projboard.models.subject import Subject
from projboard.models.article import Article, Like

TITLE = "Article Test"
CONTENT = "I'm not gonna write all that!"
SUBJECT = "TEST"
NAME = "Shalev"


@pytest.mark.django_db
class TestLikeModel:

    @pytest.fixture
    @pytest.mark.django_db
    def create_subject(self):
        subject = Subject(name=SUBJECT)
        subject.save()
        return subject

    @pytest.fixture
    @pytest.mark.django_db
    def create_user(self):
        user = User(name=NAME, nickname=f"{NAME}os", email=f"{NAME}@mail.com", password="f{NAME}123")
        user.save()
        return user

    @pytest.fixture
    @pytest.mark.django_db
    def create_article(self, create_user, create_subject):
        article = Article(user_id=create_user, title=TITLE, content=CONTENT, subject_id=create_subject)
        article.save()
        return article

    @pytest.fixture
    @pytest.mark.django_db
    def create_like(self, create_user, create_article):
        like = Like(user_id=create_user, article_id=create_article)
        like.save()
        return like

    def test_create_like(self, create_like):
        assert create_like in Like.objects.all()
        assert create_like.article_id.title == TITLE
        assert create_like.user_id.name == NAME

    def test_delete_like(self, create_user, create_like):
        result = Like.delete_like(create_like.user_id, create_like.article_id)
        assert result  # check if method delete_like success to delete the object

        assert create_like not in Like.objects.all()  # check that the object is not in the db
        result = Like.delete_like(create_user, create_like.article_id)
        assert not result  # check if method delete_like failed to delete the object

    @pytest.mark.django_db
    def test_amount_of_likes_article(self, create_like):
        amount_likes = Like.amount_of_likes_article(create_like.article_id)
        assert len(Like.objects.filter(article_id=create_like.article_id)) == amount_likes

        Like.delete_like(create_like.user_id, create_like.article_id)
        assert Like.objects.filter(article_id=create_like.article_id).count() != amount_likes
