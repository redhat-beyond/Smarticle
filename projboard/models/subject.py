from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Subject(models.Model):
    """
    Subject model
    name- A string, the subject name
    """
    name = models.CharField(max_length=100)

    @staticmethod
    def get_subject_by_name(name):
        """
        Method get subject name and return Subject object if exist, otherwise None
        :param name: the name to search
        :return: Subject object
        """
        try:
            subject = Subject.objects.get(name=name)
        except ObjectDoesNotExist:
            return None
        return subject

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def get_list_subjects_names():
        """
        Method get list subject names
        :return: the list of subject
        """
        subjects_list = list(Subject.objects.all().values_list('name', flat=True))
        return subjects_list

    @staticmethod
    def create_and_get_subject(name):
        """
        Method create a new subject
        :param name: The name of the subject
        :return: the subject that created
        """
        try:
            subject = Subject.objects.get(name=name)
            return subject
        except Subject.DoesNotExist:
            subject = Subject(name=name)
            subject.save()
            return subject

    @staticmethod
    def rename_subject(existing_name, new_name):
        """
        Method rename the subject name
        :param existing_name: The name of the existing subject
        :param new_name: The new name of the subject
        :return: The new name of the subject
        """
        try:
            subject = Subject.objects.get(name=existing_name)
            subject.name = new_name
            subject.save()
            return subject
        except Subject.DoesNotExist:
            return None

    @staticmethod
    def delete_subject(name):
        """
        Method delete a subject
        :param name: The name of the subject
        :return: True if success
        """
        try:
            subject = Subject.objects.get(name=name)
            subject.delete()
            return True
        except Subject.DoesNotExist:
            return False
