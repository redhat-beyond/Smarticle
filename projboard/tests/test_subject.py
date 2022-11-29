import pytest
from projboard.models import Subject

SPORT = "sport"
ANIMALS = "Animals"
NOTEXIST = "notexist"
REDHAT = "redhat"


@pytest.fixture
def generate_subject(name='name'):
    subject = Subject(name=name)
    subject.save()
    return subject


class TestSubjectModel:
    @pytest.mark.django_db
    def test_create_subject(db):
        subject = Subject.create_new_subject(SPORT)
        assert subject.name == SPORT

        subject = Subject.create_new_subject(SPORT)
        assert subject.name == SPORT

    @pytest.mark.django_db
    def test_update_subject(self, generate_subject):
        Subject.create_new_subject(generate_subject)
        subject = Subject.edit_subject(generate_subject, ANIMALS)
        assert subject.name == ANIMALS

        subject = Subject.edit_subject(NOTEXIST, ANIMALS)
        assert not subject

    @pytest.mark.django_db
    def test_delete_subject(self, generate_subject):
        result = Subject.delete_subject(NOTEXIST)
        assert not result

        subject = Subject.create_new_subject(generate_subject)
        result = Subject.delete_subject(subject.name)
        assert result

    @pytest.mark.django_db
    def test_get_list_subjects_names(self, generate_subject):
        subject = Subject.create_new_subject(generate_subject)
        subject1 = Subject.create_new_subject(ANIMALS)
        subject2 = Subject.create_new_subject(REDHAT)
        listSubject = Subject.get_list_subjects_names()
        assert subject.name in listSubject
        assert subject1.name in listSubject
        assert subject2.name in listSubject
