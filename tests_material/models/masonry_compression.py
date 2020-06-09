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

class MasonryCompression(models.Model):
    BRICK_CHOICES = (
        ("LADRILLO_UNIDAD_HUECA", "Ladrillo Unidad Hueca"),
        ("LADRILLO_UNIDAD_SOLIDA", "Ladrillo Unidad Solida"),
        ("BLOQUE_UNIDAD_HUECA", "Bloque Unidad Hueca"),
    )
    brick_type      = models.CharField(max_length=50, choices=BRICK_CHOICES, default="LADRILLO_UNIDAD_HUECA",)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Compresion de Albañileria")
    element_name    = models.CharField(max_length=100, null=True, blank=True)
    code            = models.CharField(max_length=255, unique=True, editable=False)
    sampling_date   = models.DateField(default=datetime.datetime.now, null=True, blank=True)
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

        super(MasonryCompression, self).save(*args, **kwargs)

    def __str__(self):
        return f"Compresion de Albañileria {self.id}"


class Masonry(models.Model):
    poured_date     = models.DateField()
    break_date      = models.DateField()
    element_name    = models.CharField(max_length=40)
    dilate          = models.IntegerField(editable=False)
    L               = models.FloatField()
    A               = models.FloatField()
    hp              = models.FloatField()
    tp              = models.FloatField()
    hp_tp           = models.FloatField(editable=False)
    correction      = models.FloatField(editable=False)
    area            = models.FloatField(editable=False)
    load            = models.FloatField()
    fc              = models.FloatField(editable=False)
    fc_MPa          = models.FloatField(editable=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    masonry_compression = models.ForeignKey(MasonryCompression, on_delete=models.CASCADE)
    equipment       = models.ManyToManyField(Equip)
    tool            = models.ManyToManyField(Tool)

    def save(self, *args, **kwargs):
        # Generate the dilate from the poured_date
        diff = self.break_date - self.poured_date
        self.dilate = diff.days

        # Generate the area
        area_cm2 = (self.L*0.1) * (self.A*0.1)
        self.area = round(area_cm2, 2)

        # Generate the hp_tp
        hp_tp_factor = self.hp / self.tp
        self.hp_tp = round(hp_tp_factor, 1)

        # Generate correction
        x_ld = [1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
        y_correction = [0.75, 0.86, 1.00, 1.04, 1.07, 1.15, 1.22]
        correc = np.interp(self.hp_tp, x_ld, y_correction)
        self.correction = round(correc, 2)

        # Generate the fc
        effort_fc = (self.load / self.area) * self.correction
        self.fc = round(effort_fc, 2)

        # Generate fc_MPa
        effort_fc_MPa = self.fc * 0.0981
        self.fc_MPa = round(effort_fc_MPa, 1)

        super(Masonry, self).save(*args, **kwargs)

    def __str__(self):
        return f"Albañileria {self.id}"
