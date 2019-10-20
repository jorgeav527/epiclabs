from django.db import models

from accounts.models import ClientProfile

# Create your models here.

class ReferencePerson(models.Model):
    TITLE_CHOICES = (
        ("NN", "Ninguna"),
        ("O", "Operario"),
        ("T", "Técnico"),
        ("I", "Ingeniero"),
        ("M", "Magister"),
    )

    title   = models.CharField(max_length=5, choices=TITLE_CHOICES, default="NN")
    name    = models.CharField(max_length=50)
    dni     = models.CharField(max_length=50)
    phone   = models.CharField(max_length=20)
    ClientProfile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}-{self.name}"