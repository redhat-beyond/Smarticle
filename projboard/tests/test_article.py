import pytest
from projboard.models.article import Article, Like, View_Article, Subject, User
from django.db.models import Count


TITLE = "Article Test"
CONTENT = "I'm not gonna write all that!"


class TestArticle:

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
        user = User(name="Anas", nickname="A99", email="Anas@gmail.com", password="Anas123")
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

    @pytest.mark.django_db
    def test_part_functions(self, create_articles):
        article = create_articles[0]
        # testing @property functions => PartOf..()
        # whent title & content length is less than reality
        assert article.part_of_title(5) == article.title[:5] + '...'
        assert article.part_of_content(5) == article.content[:5] + '...'
        # whent title & content length is greater than reality
        assert article.part_of_title(100) == article.title[:100]
        assert article.part_of_content(100) == article.content[:100]

    @pytest.mark.django_db
    def test_object_saved_in_db(self, create_articles):
        assert create_articles[0] in Article.objects.all()
        assert create_articles[1] in Article.objects.all()

    @pytest.mark.django_db
    # using Edite function
    def test_edit_object(self, create_articles, create_subjects):

        article = create_articles[0]
        title = "New Title"
        content = "New Content"
        subject = create_subjects[1]
        old_subject = create_subjects[0]

        assert article.subject_id == old_subject

        article.edit(title, content, subject)

        assert article.title == title
        assert article.content == content
        assert article.subject_id == subject
        # if subject not in Article.SUBJECTS the value won't be changed
        unsaved_subject = Subject(name='k')
        article.edit(subject=unsaved_subject)
        assert article.subject_id == subject

    @pytest.mark.django_db
    def test_search_objects(self, create_articles, create_subjects, create_user):
        user1 = create_user[1]
        article_list = [i for i in create_articles]
        subject1 = create_subjects[1]

        # search by title or a part of it
        assert article_list[1] in Article.search_by_title("Test")

        # search by user
        assert article_list[1] in Article.search_by_user(user1)

        # search by subject
        assert article_list[1] in Article.search_by_subject(subject1)

    @pytest.mark.django_db
    def test_search_objects_none_exists(self, create_articles, create_subjects, create_user):
        # if not in db
        user1 = create_user[1]
        article_list = [i for i in create_articles]
        subject1 = create_subjects[1]

        # search by title or a part of it
        assert article_list[1] not in Article.search_by_title("Hakuna matata")

        # search by user
        assert article_list[0] not in Article.search_by_user(user1)

        # search by subject
        assert article_list[0] not in Article.search_by_subject(subject1)

    @pytest.fixture
    @pytest.mark.django_db
    def create_like(self, create_user, create_articles):
        like = Like(user_id=create_user[0], article_id=create_articles[0])
        like.save()
        return like

    @pytest.fixture
    @pytest.mark.django_db
    def create_view(self, create_user, create_articles):
        view_article = View_Article(user_id=create_user[0], article_id=create_articles[0])
        view_article.save()
        return view_article

    @pytest.mark.django_db
    def test_filter_by_likes(self, create_like):
        """
        Filter By Likes
        filter_by_likes() return look like => [(article object, int (num_of_likes)), ...]
        """
        filtered_articles = [i[1] for i in Article.filter_by_likes()]
        """
        filtered_articles look like => [ int, int, int, ....] => list of num_of_views of all article objects
        """
        assert sorted(filtered_articles, reverse=True) == filtered_articles

    @pytest.mark.django_db
    def test_filter_by_views(self, create_view):
        """
        Filter By Views
        filter_by_views() return look view => [(article object, int (num_of_views)), ...]
        """
        filtered_articles = [i[1] for i in Article.filter_by_views()]
        """
        filtered_articles look like => [ int, int, int, ....] => list of num_of_views of all article objects
        """
        assert sorted(filtered_articles, reverse=True) == filtered_articles

    @pytest.mark.django_db
    def test_get_num_of_likes(self, create_articles, create_like, create_view):
        article = create_articles[0]

        assert Like.objects.filter(article_id=article).values(
            'article_id').annotate(num_likes=Count('article_id'))[0]['num_likes'] == article.num_of_likes()

    @pytest.mark.django_db
    def test_get_num_of_views(self, create_articles, create_like, create_view):
        article = create_articles[0]

        assert View_Article.objects.filter(article_id=article).values(
            'article_id').annotate(num_views=Count('article_id'))[0]['num_views'] == article.num_of_views()
