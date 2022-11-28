import pytest
from projboard.models import Subject

SPORT = "sport"
ANIMALS = "Animals"
NOTEXIST = "notexist"
REDHAT = "redhat"


class TestSubjectModel:
    @pytest.mark.django_db
    def test_create_subject(db):
        subject = Subject.create_new_subject(name=SPORT)
        assert subject.name == SPORT

        subject = Subject.create_new_subject(name=SPORT)
        assert subject.name == SPORT

    @pytest.mark.django_db
    def test_update_subject(db):
        Subject.create_new_subject(name=SPORT)
        subject = Subject.edit_subject(SPORT, ANIMALS)
        assert subject.name == ANIMALS

        subject = Subject.edit_subject(NOTEXIST, ANIMALS)
        assert not subject

    @pytest.mark.django_db
    def test_delete_subject(db):
        result = Subject.delete_subject(NOTEXIST)
        assert not result

        subject = Subject.create_new_subject(SPORT)
        result = Subject.delete_subject(subject.name)
        assert result

    @pytest.mark.django_db
    def test_get_list_subjects_names(db):
        subject = Subject.create_new_subject(SPORT)
        subject1 = Subject.create_new_subject(ANIMALS)
        subject2 = Subject.create_new_subject(REDHAT)
        listSubject = Subject.get_list_subjects_names()
        assert subject.name in listSubject
        assert subject1.name in listSubject
        assert subject2.name in listSubject
