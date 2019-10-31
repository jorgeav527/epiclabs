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

class DiamondPiceBreak(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Compresión Testigo Diamantinos")
    element         = models.CharField(max_length=50, null=True, blank=True)
    code            = models.CharField(max_length=255, unique=True, editable=False)
    fc_esp          = models.FloatField(default=280)
    extraction_data = models.DateField()
    break_data      = models.DateField(default=datetime.datetime.now)
    duration        = models.IntegerField(editable=False)
    D               = models.FloatField()
    L               = models.FloatField()
    factor_ld       = models.FloatField(editable=False)
    correction      = models.FloatField(editable=False)
    area            = models.FloatField(editable=False)
    F               = models.FloatField()
    fc              = models.FloatField(editable=False)
    fc_MPa          = models.FloatField(editable=False)
    fc_175          = models.FloatField(editable=False)
    fc_210          = models.FloatField(editable=False)
    fc_280          = models.FloatField(editable=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    equipment           = models.ManyToManyField(Equip)
    tool                = models.ManyToManyField(Tool)    
    course              = models.ForeignKey(Course, models.SET_NULL, null=True, blank=True)
    reference_person    = models.ForeignKey(ReferencePerson, models.SET_NULL, null=True, blank=True)
    construction        = models.ForeignKey(Construction, models.SET_NULL, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Generate the code for the barcode (e.g. RDC2009092701)
        date = datetime.datetime.today()
        letters = ""
        words = self.name.split()
        for word in words:
            letters += word[0]
        self.code = f"{letters.upper()}{date.year}{date.month}{date.day}{date.hour}{date.minute}{date.second}"

        # Generate the duration from the poured_data
        diff = self.break_data - self.extraction_data
        self.duration = diff.days

        # Generate the area from the avg largo and ancho
        factor = self.L / self.D
        self.factor_ld = round(factor, 2) 

        # Generate the area from the avg largo and ancho
        d_cm = self.D*2.54
        area_cm2 = ((d_cm**2)*math.pi)/4
        self.area = round(area_cm2, 2)
        
        # Generate the correction factor
        x_ld = [1, 1.25, 1.50, 1.75]
        y_correction = [0.87, 0.93, 0.96, 0.98]
        correction = np.interp(self.factor_ld, x_ld, y_correction)
        self.correction = round(correction, 2)

        # Generate the fc
        effort_fc = ( self.F / self.area ) * self.correction
        self.fc = round(effort_fc, 2)

        # Generate fc_MPa
        effort_fc_MPa = self.fc*0.0981 
        self.fc_MPa = round(effort_fc_MPa, 2)

        # Generate the fc_175
        effort_fc_175 = (self.fc/175)*100 
        self.fc_175 = round(effort_fc_175, 2)

        # Generate the fc_210
        effort_fc_210 = (self.fc/210)*100 
        self.fc_210 = round(effort_fc_210, 2)

        # Generate the fc_280
        effort_fc_280 = (self.fc/280)*100 
        self.fc_280 = round(effort_fc_280, 2)

        super(DiamondPiceBreak, self).save(*args, **kwargs)

    def __str__(self):
        return f"Testigo de Diamantino {self.id}"