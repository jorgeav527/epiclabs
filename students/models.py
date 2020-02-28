from django.db import models

from accounts.models import GroupProfile

# Create your models here.

class Student(models.Model):
    full_name   = models.CharField(max_length=64)
    codigo      = models.BigIntegerField()
    email       = models.EmailField(null=True, blank=True,)
    phone       = models.BigIntegerField(null=True, blank=True,)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    group_profile = models.ForeignKey(GroupProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name} {self.codigo}"
