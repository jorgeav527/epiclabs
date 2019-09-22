from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    User,
    StudentProfile,
    BachProfile,
    TeacherProfile,
    ClientProfile,
    AdminProfile,
)

# Create your signals

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if instance.is_student:
        if created:
            StudentProfile.objects.create(user=instance)
        else:
            instance.studentprofile.save()
    elif instance.is_bach:
        if created:
            BachProfile.objects.create(user=instance)
        else:
            instance.bachprofile.save()
    elif instance.is_teacher:
        if created:
            TeacherProfile.objects.create(user=instance)
        else:
            instance.teacherprofile.save()
    elif instance.is_client:
        if created:
            ClientProfile.objects.create(user=instance)
        else:
            instance.clientprofile.save()
    elif instance.is_admin:
        if created:
            AdminProfile.objects.create(user=instance)
        else:
            instance.adminprofile.save()

