import pytest
from projboard.models.subject import Subject

ANIMALS = "Animals"
NOT_EXIST = "not_exist"


@pytest.mark.django_db
class TestSubjectModel:

    def test_create_subject(self, subjects):
        assert subjects[0] in Subject.objects.all()
        assert subjects[1] in Subject.objects.all()

    def test_delete_subject(self, subjects):
        Subject.delete_subject(subjects[0])
        assert subjects[0] not in Subject.objects.all()

    def test_update_subject(self, subjects):
        subject = Subject.rename_subject(subjects[0], ANIMALS)
        assert subject.name == ANIMALS

        subject = Subject.rename_subject(NOT_EXIST, ANIMALS)
        assert not subject

    def test_get_list_subjects_names(self, subjects):
        listSubject = Subject.get_list_subjects_names()
        for i in subjects:
            assert i.name in listSubject
