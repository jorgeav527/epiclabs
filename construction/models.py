from django.db import models
import datetime

# Create your models here.

from accounts.models import ClientProfile

class Construction(models.Model):
    name            = models.CharField(max_length=150)
    location        = models.CharField(max_length=150)
    reference       = models.CharField(max_length=150)
    start_day       = models.DateField(default=datetime.datetime.now)
    finish_day      = models.DateField()
    duration        = models.IntegerField(editable=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    client_profile  = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        diff = self.finish_day - self.start_day
        duration = diff.days 

        super(Thesis, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
