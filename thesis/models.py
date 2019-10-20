from django.db import models
import datetime

from accounts.models import BachProfile, TeacherProfile
from course.models import Course


# Create your models here.

class Thesis(models.Model):
    LINE_CHOICES = (
        ("NN", "Ninguna"),
        ("TC", "Agregados"),
        ("S", "Geotecnia"),
        ("MC", "Mecánica de Materiales"),
        ("TM", "Tecnologías Modernas"),
    )
    title           = models.CharField(max_length=300)
    line            = models.CharField(max_length=5, choices=LINE_CHOICES, default="NN")
    course          = models.ManyToManyField(Course)
    adviser         = models.ManyToManyField(TeacherProfile)
    start_day       = models.DateField(default=datetime.datetime.now)
    finish_day      = models.DateField()
    duration        = models.IntegerField(editable=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    bach_profile    = models.ForeignKey(BachProfile, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        diff = self.finish_day - self.start_day
        duration = diff.days 

        super(Thesis, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"