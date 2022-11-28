import pytest
from projboard.models import User,Article,Like,View,Subject

TITLE = "Article Test"
CONTENT = "I'm not gonna write all that!"

class TestArticle :

    @pytest.fixture
    def sup(self):
        return Subject(name = 'N')

    @pytest.fixture
    def sup1(self):
        return Subject(name = 'R')
    
    @pytest.fixture
    def user(self):
        return User(name = "Anas", nickname = "A99" , email = "Anas@gmail.com" , password = "Anas123")
    
    @pytest.fixture
    def art(self,user, sup):
        return Article(user_id = user, title = TITLE, content = CONTENT, subject_id = sup )

    @pytest.mark.skip
    def test_objectCreation(self,user, art):
        assert art.title == TITLE
        assert art.content == CONTENT
        # testing __str__ function
        assert art.__str__() == art.title 
    
    @pytest.mark.skip
    def test_PartFunctions(self,art):
        # testing @property functions => PartOf..()
        # whent title & content length is less than reality 
        assert art.PartOfTitle(5) == art.title[:5]+ '...'
        assert art.PartOfContent(5) == art.content[:5]+ '...'
        # whent title & content length is greater than reality
        assert art.PartOfTitle(100) == art.title[:100]
        assert art.PartOfContent(100) == art.content[:100]
        
    
    @pytest.mark.skip
    @pytest.mark.django_db
    def test_objectSavedInDb(self, user, art, sup):
        sup.save()
        user.save()
        art.save()
        assert art in Article.objects.all()
    
    @pytest.mark.skip
    @pytest.mark.django_db
    # using Edite function 
    def test_EditeObject(self,user, art, sup, sup1):
        sup.save()
        sup1.save()
        user.save()
        art.save()

        title = "New Title"
        content = "New Content"
        subject = sup1

        assert art.subject_id == sup

        art.Edite(title, content, subject)

        assert art.title == title
        assert art.content == content
        assert art.subject_id == sup1
        # if subject not in Article.SUBJECTS the value won't be changed 
        subject = Subject(name = 'k')
        art.Edite(subject = subject)
        assert art.subject_id == sup1
    
    
    @pytest.fixture
    def user1(self):
        return User(name = "John", nickname = "J99" , email = "John@gmail.com" , password = "John123")

    @pytest.fixture
    def art1(self,user1,sup1):
        return Article(user_id = user1, title = "RED HAT", content = CONTENT, subject_id = sup1 )

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_searchObjects(self, user, art, user1, art1, sup,sup1):
        sup.save()
        sup1.save()
        user.save()
        user1.save()
        art.save()
        art1.save()
        

        # search by title or a part of it 
        assert art1 in Article.searchByTitle("RED")
        assert art not in Article.searchByTitle("RED")

        # search by user
        assert art1 in Article.searchByUser(user1)
        assert art not in Article.searchByUser(user1)

        # search by subject
        assert art1 in Article.searchBySubject(sup1)
        assert art not in Article.searchBySubject(sup1)
    
    @pytest.fixture
    def like(self,user,art):
        return Like(user,art)
    
    @pytest.fixture
    def view(self,user,art):
        return View(user,art)

    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_filterObjects(self,sup, sup1, user, art,user1,  art1, like, view):
        sup.save()
        sup1.save()
        user.save()
        art.save() 
        like.save()
        view.save()
        user1.save()
        art1.save()
        # Filter By Likes
        assert art != Article.filterByLikes()[0]
        assert art1 in Article.filterByLikes()
        # Filter By Views
        assert art == Article.filterByViews()[0]
        assert art1 in Article.filterByViews()
    
    # @pytest.mark.skip
    # @pytest.mark.django_db
    # def test_getNumOfFuntions(self, user, user1, art1, art, like, view):
    #     user.save()
    #     art.save()
    #     user1.save()
    #     art1.save()

    #     like.save()
    #     view.save()
        
    #     assert 1 != art.numOfLikes()
    #     assert 0 != art1.numOfLikes()
        