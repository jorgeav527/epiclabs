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


class PrismBreak(models.Model):
    COMPOSITION_CHOICES = (
        ("DADO_CONCRETO", "Dado de Concreto"),
        ("DADO_CAL", "Dado de Cal"),
        ("ROCA", "Roca"),
        ("ADOQUIN_CONCRETO", "Adoquin de Concreto"),
    )
    prism_type      = models.CharField(max_length=20, choices=COMPOSITION_CHOICES, default="DADO_CONCRETO",)
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

        super(PrismBreak, self).save(*args, **kwargs)

    def __str__(self):
        return f"Prisma {self.id}"


class Prism(models.Model):
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
    prism_break      = models.ForeignKey(PrismBreak, on_delete=models.CASCADE)
    equipment       = models.ManyToManyField(Equip)
    tool            = models.ManyToManyField(Tool)

    def save(self, *args, **kwargs):
        # Generate the dilate from the poured_date
        diff = self.break_date - self.poured_date
        self.dilate = diff.days

        # Generate the area
        avg_D = (self.D_1*0.1) * (self.D_2*0.1)
        self.area = round(avg_D, 2)

        # Generate the fc
        effort_fc = self.load / self.area
        self.fc = round(effort_fc, 2)

        # Generate fc_MPa
        effort_fc_MPa = self.fc * 0.0981 
        self.fc_MPa = round(effort_fc_MPa, 1)

        super(Prism, self).save(*args, **kwargs)

    def __str__(self):
        return f"Prismas {self.id}"


