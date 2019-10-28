from django.db import models

from accounts.models import ClientProfile

# Create your models here.

class ReferencePerson(models.Model):
    title   = models.CharField(max_length=10)
    name    = models.CharField(max_length=50)
    dni     = models.BigIntegerField(null=True, blank=True,)
    phone   = models.BigIntegerField(null=True, blank=True,)
    client_profile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.name.title()}"