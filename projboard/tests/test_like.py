import pytest
from projboard.models.article import Like


TITLE = "Article Test"
NAME = "my_username"


@pytest.mark.django_db
class TestLikeModel:

    def test_create_like(self, like):
        assert like in Like.objects.all()
        assert like.article_id.title == TITLE
        assert like.user_id.name == NAME

    def test_delete_like(self, users, like):
        result = Like.delete_like(like.user_id, like.article_id)
        assert result  # check if method delete_like success to delete the object

        assert like not in Like.objects.all()  # check that the object is not in the db
        result = Like.delete_like(users[0], like.article_id)
        assert not result  # check if method delete_like failed to delete the object

    def test_amount_of_likes_article(self, like):
        amount_likes = Like.amount_of_likes_article(like.article_id)
        assert len(Like.objects.filter(article_id=like.article_id)) == amount_likes

        Like.delete_like(like.user_id, like.article_id)
        assert len(Like.objects.filter(article_id=like.article_id)) != amount_likes
