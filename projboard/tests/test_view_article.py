import pytest
from projboard.models.article import View_Article


@pytest.mark.django_db
class TestViewModel:

    def test_create_view(self, view):
        assert view in View_Article.objects.all()

    def test_amount_of_views_article(self, view):
        amount_views = View_Article.amount_of_views_article(view.article_id)
        assert len(View_Article.objects.filter(article_id=view.article_id)) == amount_views
