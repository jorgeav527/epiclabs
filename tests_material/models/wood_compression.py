from django.db import models
import datetime
import math
import numpy as np

from accounts.models import User
from equipments.models import Equip
from tools.models import Tool
from reference_person.models import ReferencePerson
from construction.models import Construction
from course.models import Course

class WoodCompression(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Compresion de Madera")
    name_element    = models.CharField(max_length=50, null=True, blank=True)
    wood_name       = models.CharField(max_length=100, null=True, blank=True)
    code            = models.CharField(max_length=255, unique=True, editable=False)
    sampling_date   = models.DateField()
    done_date       = models.DateField(default=datetime.datetime.now)
    dilate          = models.IntegerField(editable=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    equipment           = models.ManyToManyField(Equip)
    tool                = models.ManyToManyField(Tool)    
    course              = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    reference_person    = models.ForeignKey(ReferencePerson, on_delete=models.SET_NULL, null=True, blank=True)
    construction        = models.ForeignKey(Construction, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):

        # Generate the code for the barcode (e.g. RDC2009092701)
        date = datetime.datetime.today()
        letters = ""
        words = self.name.split()
        for word in words:
            letters += word[0]
        self.code = f"{letters.upper()}{date.year}{date.month}{date.day}{date.hour}{date.minute}{date.second}"

        # Generate the duration from the poured_data
        diff = self.done_date - self.sampling_date
        self.dilate = diff.days

        super(WoodCompression, self).save(*args, **kwargs)

    def __str__(self):
        return f"Compresion de Madera {self.id}"


class ParallelPerpendicular(models.Model):
    POSITION_CHOICES = (
        ("NINGUNA", "Ninguna"),
        ("PARALELO", "Comprecíon Paralelo a la Fibra"),
        ("PERPENDICULAR", "Compreción Perpendicular a la Fibra"),
    )
    type_compression = models.CharField(max_length=40, choices=POSITION_CHOICES, default="NINGUNA",)
    name_element    = models.CharField(max_length=40)
    length_1        = models.FloatField()
    width_1         = models.FloatField()
    area_1          = models.FloatField(editable=False)
    length_2        = models.FloatField()
    width_2         = models.FloatField()
    area_2          = models.FloatField(editable=False)
    average_area    = models.FloatField(editable=False)
    load            = models.FloatField()
    fc              = models.FloatField(editable=False)
    fc_MPa          = models.FloatField(editable=False)
    wood_compression = models.ForeignKey(WoodCompression, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)


    def save(self, *args, **kwargs):

        # Generate area_1
        a_1 = (self.length_1*0.1) * (self.width_1*0.1)
        self.area_1 = round(a_1, 2)

        # Generate area_2
        a_2 = (self.length_2*0.1) * (self.width_2*0.1) 
        self.area_2 = round(a_2, 2)
        
        # Generate average_area
        aa = (self.area_1 + self.area_2) / 2
        self.average_area = round(aa, 2)

        # Generate compression_resistance
        fc = self.load / self.average_area
        self.fc = round(fc, 2)

        # Generate fc_MPa
        fc_MPa = self.fc*0.0981 
        self.fc_MPa = round(fc_MPa, 1)

        super(ParallelPerpendicular, self).save(*args, **kwargs)

    def __str__(self):
        return f"Paralelo y Perpendicular {self.id}"