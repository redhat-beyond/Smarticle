import pytest
from projboard.models.article import Article, Like, View_Article, Subject
from django.db.models import Count
from enum import Enum


# Enum to deal with not existed objects
class DataType(Enum):
    EXIST, NON_EXIST = range(0, 2)


@pytest.mark.django_db
class TestArticle:

    def test_part_functions(self, article):
        # testing @property functions => PartOf..()
        # whent title & content length is less than reality
        assert article.part_of_title(5) == article.title[:5] + '...'
        assert article.part_of_content(5) == article.content[:5] + '...'
        # whent title & content length is greater than reality
        assert article.part_of_title(100) == article.title[:100]
        assert article.part_of_content(100) == article.content[:100]

    def test_object_saved_in_db(self, articles):
        for i in range(len(articles)):
            assert articles[i] in Article.objects.all()

    # using Edit function
    def test_edit_article(self, article, subject):
        title = "New Title"
        content = "New Content"
        article.edit(title, content, subject)

        assert article.title == title
        assert article.content == content
        assert article.subject_id == subject
        # if subject not in Article.SUBJECTS the value won't be changed
        unsaved_subject = Subject(name='k')
        article.edit(subject=unsaved_subject)
        assert article.subject_id == subject

    def test_search_by_object(self, articles, subjects, users):
        # Assign articles for user
        article_list = [i for i in articles]
        for i in range(len(article_list)):
            assert article_list[i] in Article.search_by_title("Test")
            assert article_list[i] in Article.search_by_user(users[i])
            assert article_list[i] in Article.search_by_subject(subjects[i])

    def test_search_non_exist_keys(self, articles, subjects, users):
        # if not in db
        not_existed_user = users[DataType.NON_EXIST.value]
        article_list = [i for i in articles]
        not_existed_subject = subjects[DataType.NON_EXIST.value]

        # search by title or a part of it
        assert article_list[1] not in Article.search_by_title("Hakuna matata")

        # search by user
        assert article_list[0] not in Article.search_by_user(not_existed_user)

        # search by subject
        assert article_list[0] not in Article.search_by_subject(not_existed_subject)

    def test_filter_by_likes(self, like):
        """
        Filter By Likes
        filter_by_likes() return look like => [(article object, int (num_of_likes)), ...]
        """
        filtered_articles = [i[1] for i in Article.filter_by_likes()]
        """
        filtered_articles look like => [ int, int, int, ....] => list of num_of_views of all article objects
        """
        assert sorted(filtered_articles, reverse=True) == filtered_articles

    def test_filter_by_views(self, view):
        """
        Filter By Views
        filter_by_views() return look view => [(article object, int (num_of_views)), ...]
        """
        filtered_articles = [i[1] for i in Article.filter_by_views()]
        """
        filtered_articles look like => [ int, int, int, ....] => list of num_of_views of all article objects
        """
        assert sorted(filtered_articles, reverse=True) == filtered_articles

    def test_get_num_of_likes(self, article, like, view):
        my_article = article

        assert Like.objects.filter(article_id=my_article).values(
            'article_id').annotate(num_likes=Count('article_id'))[0]['num_likes'] == my_article.num_of_likes()

    def test_get_num_of_views(self, article, like, view):
        my_article = article

        assert View_Article.objects.filter(article_id=my_article).values(
            'article_id').annotate(num_views=Count('article_id'))[0]['num_views'] == my_article.num_of_views()
