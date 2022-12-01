import pytest
from projboard.models.subject import Subject

ANIMALS = "Animals"
NOTEXIST = "notexist"
REDHAT = "redhat"
NAME = "yael"


@pytest.fixture
@pytest.mark.django_db
def generate_subject():
    subject = Subject.create_and_get_subject(name="yael")
    subject.save()
    return subject


@pytest.fixture
@pytest.mark.django_db
def generate_subjects(generate_subject):
    subject = Subject.create_and_get_subject(name="gal")
    subject.save()
    return [subject, generate_subject]


@pytest.mark.django_db
class TestSubjectModel:
    def test_create_subject(self, generate_subject):
        assert generate_subject in Subject.objects.all()

    def test_delete_subject(self, generate_subject):
        Subject.delete_subject(generate_subject)
        assert generate_subject not in Subject.objects.all()

    def test_update_subject(self, generate_subject):
        subject = Subject.rename_subject(generate_subject, ANIMALS)
        assert subject.name == ANIMALS

        subject = Subject.rename_subject(NOTEXIST, ANIMALS)
        assert not subject

    @pytest.mark.django_db
    def test_get_list_subjects_names(self, generate_subjects):
        listSubject = Subject.get_list_subjects_names()
        for i in generate_subjects:
            assert i.name in listSubject
