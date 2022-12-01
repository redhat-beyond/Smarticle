import pytest
from projboard.models.article import View, User, Article, Subject


TITLE = "Article Test"
CONTENT = "Anas not gonna write all that!"
NAME = "Amit"


@pytest.mark.django_db
class TestViewModel:

    @pytest.fixture
    @pytest.mark.django_db
    def create_subjects(self):
        subject = Subject(name='N')
        subject.save()
        return subject

    @pytest.fixture
    @pytest.mark.django_db
    def create_user(self):
        user = User(name=NAME, nickname="A98", email="Amit@gmail.com", password="Amit")
        user.save()
        return user

    @pytest.fixture
    @pytest.mark.django_db
    def create_articles(self, create_user, create_subjects):
        article = Article(user_id=create_user, title=TITLE, content=CONTENT, subject_id=create_subjects)
        article.save()
        return article

    @pytest.fixture
    @pytest.mark.django_db
    def create_view(self, create_user, create_articles):
        view = View(user_id=create_user, article_id=create_articles)
        view.save()
        return view

    @pytest.mark.django_db
    def test_create_view(self, create_view):
        assert create_view in View.objects.all()

    @pytest.mark.django_db
    def test_amount_of_views_article(self, create_view):
        amount_views = View.amount_of_views_article(create_view.article_id)
        assert len(View.objects.filter(article_id=create_view.article_id)) == amount_views
