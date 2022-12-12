import pytest
from projboard.models.subject import Subject

ANIMALS = "Animals"
NOT_EXIST = "not_exist"


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

        subject = Subject.rename_subject(NOT_EXIST, ANIMALS)
        assert not subject

    def test_get_list_subjects_names(self, generate_subjects):
        listSubject = Subject.get_list_subjects_names()
        for i in generate_subjects:
            assert i.name in listSubject
