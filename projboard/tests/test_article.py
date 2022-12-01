import pytest
from projboard.models.article import Article, Like, View, Subject, User
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

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_objectCreation(self, create_articles):
        article = create_articles[0]
        assert article.title == TITLE
        assert article.content == CONTENT
        # testing __str__ function
        assert article.__str__() == article.title

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_PartFunctions(self, create_articles):
        article = create_articles[0]
        # testing @property functions => PartOf..()
        # whent title & content length is less than reality
        assert article.PartOfTitle(5) == article.title[:5] + '...'
        assert article.PartOfContent(5) == article.content[:5] + '...'
        # whent title & content length is greater than reality
        assert article.PartOfTitle(100) == article.title[:100]
        assert article.PartOfContent(100) == article.content[:100]

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_objectSavedInDb(self, create_articles):
        assert create_articles[0] in Article.objects.all()
        assert create_articles[1] in Article.objects.all()

    # @pytest.mark.skip
    @pytest.mark.django_db
    # using Edite function
    def test_EditObject(self, create_articles, create_subjects):

        article = create_articles[0]
        title = "New Title"
        content = "New Content"
        subject = create_subjects[1]
        old_subject = create_subjects[0]

        assert article.subject_id == old_subject

        article.Edit(title, content, subject)

        assert article.title == title
        assert article.content == content
        assert article.subject_id == subject
        # if subject not in Article.SUBJECTS the value won't be changed
        unsaved_subject = Subject(name='k')
        article.Edit(subject=unsaved_subject)
        assert article.subject_id == subject

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_searchObjects(self, create_articles, create_subjects, create_user):
        user1 = create_user[1]
        article_list = [i for i in create_articles]
        subject1 = create_subjects[1]

        # search by title or a part of it
        assert article_list[1] in Article.searchByTitle("Test")

        # search by user
        assert article_list[1] in Article.searchByUser(user1)

        # search by subject
        assert article_list[1] in Article.searchBySubject(subject1)

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_searchObjectsNoneExists(self, create_articles, create_subjects, create_user):
        # if not in db
        user1 = create_user[1]
        article_list = [i for i in create_articles]
        subject1 = create_subjects[1]

        # search by title or a part of it
        assert article_list[1] not in Article.searchByTitle("Hakuna matata")

        # search by user
        assert article_list[0] not in Article.searchByUser(user1)

        # search by subject
        assert article_list[0] not in Article.searchBySubject(subject1)

    @pytest.fixture
    @pytest.mark.django_db
    def create_like(self, create_user, create_articles):
        like = Like(user_id=create_user[0], article_id=create_articles[0])
        like.save()
        return like

    @pytest.fixture
    @pytest.mark.django_db
    def create_view(self, create_user, create_articles):
        view = View(user_id=create_user[0], article_id=create_articles[0])
        view.save()
        return view

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_filterByLikes(self, create_like):
        """
        Filter By Likes
        filterByLikes() return look like => [(article object, int (numOfLikes)), ...]
        """
        filteredArticles = [i[1] for i in Article.filterByLikes()]
        """
        filteredArticles look like => [ int, int, int, ....] => list of numOfViews of all article objects
        """
        assert sorted(filteredArticles, reverse=True) == filteredArticles

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_filterByViews(self, create_view):
        """
        Filter By Views
        filterByViews() return look view => [(article object, int (numOfViews)), ...]
        """
        filteredArticles = [i[1] for i in Article.filterByViews()]
        """
        filteredArticles look like => [ int, int, int, ....] => list of numOfViews of all article objects
        """
        assert sorted(filteredArticles, reverse=True) == filteredArticles

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_getNumOfLikes(self, create_articles, create_like, create_view):
        article = create_articles[0]

        assert Like.objects.filter(article_id=article).values(
            'article_id').annotate(num_likes=Count('article_id'))[0]['num_likes'] == article.numOfLikes()

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_getNumOfViews(self, create_articles, create_like, create_view):
        article = create_articles[0]

        assert View.objects.filter(article_id=article).values(
            'article_id').annotate(num_views=Count('article_id'))[0]['num_views'] == article.numOfViews()
