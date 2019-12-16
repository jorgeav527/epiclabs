from django.db import models

from accounts.models import GroupProfile

# Create your models here.

class StudentGroup(models.Model):
    full_name   = models.CharField(max_length=64)
    codigo      = models.BigIntegerField()
    email       = models.EmailField(null=True, blank=True,)
    phone       = models.BigIntegerField(null=True, blank=True,)
    group_profile = models.ForeignKey(GroupProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name} {self.codigo}"
