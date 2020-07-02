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


class PiceBreak(models.Model):
    COMPOSITION_CHOICES = (
        ("CONCRETO", "Testigo de Concreto"),
        ("CAL", "Testigo de Cal"),
    )
    pice_type       = models.CharField(max_length=10, choices=COMPOSITION_CHOICES, default="CONCRETO")
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    sampling_date   = models.DateField(default=datetime.datetime.now, null=True, blank=True)
    name            = models.CharField(max_length=50, default="Rotura Testigo")
    code            = models.CharField(max_length=255, unique=True, editable=False)
    fc_esp          = models.FloatField(default=280)
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

        super(PiceBreak, self).save(*args, **kwargs)

    def __str__(self):
        return f"Testigo {self.id}"


class Pice(models.Model):
    poured_date     = models.DateField()
    break_date      = models.DateField()
    dilate          = models.IntegerField(editable=False)
    element_name    = models.CharField(max_length=100, null=True, blank=True)
    check_per       = models.BooleanField()
    D_1             = models.FloatField()
    D_2             = models.FloatField()
    area            = models.FloatField(editable=False)
    load            = models.FloatField()
    fc              = models.FloatField(editable=False)
    fc_MPa          = models.FloatField(editable=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    pice_break      = models.ForeignKey(PiceBreak, on_delete=models.CASCADE)
    equipment       = models.ManyToManyField(Equip)
    tool            = models.ManyToManyField(Tool)

    def save(self, *args, **kwargs):
        # Generate the dilate from the poured_date
        diff = self.break_date - self.poured_date
        self.dilate = diff.days

        # Generate the area
        area_d1 = ((self.D_1**2)*math.pi) / 4
        area_d2 = ((self.D_1**2)*math.pi) / 4
        avg_area = ((area_d1 + area_d2) / 2)
        self.area = round(avg_area, 1)

        # Generate the fc
        effort_fc = self.load / (self.area/100)
        self.fc = round(effort_fc, 2)

        # Generate fc_MPa
        effort_fc_MPa = self.fc * 0.0981 
        self.fc_MPa = round(effort_fc_MPa, 1)

        super(Pice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Testigos {self.id}"
