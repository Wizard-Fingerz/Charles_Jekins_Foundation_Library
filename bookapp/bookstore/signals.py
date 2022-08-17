from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    # ignore if this is an existing User
    if not created:
        return
    Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()