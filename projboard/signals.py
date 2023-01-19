from django.db.models.signals import post_save
from django.contrib.auth.models import User as Custom_user
from django.dispatch import receiver
from models.user import User


@receiver(post_save, sender=Custom_user)
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)


@receiver(post_save, sender=Custom_user)
def save_custom_user(sender, instance, **kwargs):
    instance.User.save()
