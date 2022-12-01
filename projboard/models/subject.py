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
