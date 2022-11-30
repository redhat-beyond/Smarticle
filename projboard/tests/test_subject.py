import pytest
from projboard.models import Subject

ANIMALS = "Animals"
NOTEXIST = "notexist"
REDHAT = "redhat"
NAME = "yael"


@pytest.fixture
@pytest.mark.django_db
def generate_subject():
    subject1 = Subject.create_and_get_subject(name="yael")
    subject2 = Subject.create_and_get_subject(name="gal")
    subject1.save()
    subject2.save()
    return [subject1, subject2]


@pytest.mark.django_db
class TestSubjectModel:
    def test_create_subject(self, generate_subject):
        subject = generate_subject[0]
        assert subject.name == NAME

    def test_delete_subject(self, generate_subject):
        assert Subject.delete_subject(generate_subject[0])
        subject = Subject.get_subject_by_name(generate_subject[0])
        assert not subject

    def test_update_subject(self, generate_subject):
        subject = generate_subject[0]
        subject = Subject.edit_subject(generate_subject[0], ANIMALS)
        assert subject.name == ANIMALS

        subject = Subject.edit_subject(NOTEXIST, ANIMALS)
        assert not subject

    @pytest.mark.django_db
    def test_get_list_subjects_names(self, generate_subject):
        subject = generate_subject[0]
        subject1 = generate_subject[1]
        listSubject = Subject.get_list_subjects_names()
        assert subject.name in listSubject
        assert subject1.name in listSubject
