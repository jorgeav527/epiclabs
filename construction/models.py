from django.db import models

from accounts.models import ClientProfile

# Create your models here.

class Construction(models.Model):
    name            = models.CharField(max_length=300)
    location        = models.CharField(max_length=300)
    start_day       = models.DateField()
    finish_day      = models.DateField()
    duration        = models.IntegerField(editable=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    client_profile  = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        diff = self.finish_day - self.start_day
        self.duration = diff.days 

        super(Construction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name.title()}"
