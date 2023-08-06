import uuid

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance)
    except Exception as err:
        print(f'[signals.py] Error creating user profile!\n{err}')


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

#
# post_save.connect(create_profile, sender=User)
# post_save.connect(save_profile, sender=User)


# https://stackoverflow.com/questions/65908861/how-to-automatically-create-new-profile-once-a-new-user-is-created-in-django