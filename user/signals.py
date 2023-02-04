from django.db.models.signals import post_save
from .models import Profile
from django.contrib.auth.models import User


def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)


post_save.connect(createProfile, sender=User)
