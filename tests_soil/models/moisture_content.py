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

class MoistureContent(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Contenido Humedad")
    material        = models.CharField(max_length=50,)
    quarry          = models.CharField(max_length=50,)
    code            = models.CharField(max_length=255, unique=True, editable=False)
    sampling_date   = models.DateField()
    done_date       = models.DateField(default=datetime.datetime.now)
    dilate          = models.IntegerField(editable=False)
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
        diff = self.done_date - self.sampling_date
        self.dilate = diff.days

        super(MoistureContent, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Contenido Humedad {self.id}"


class MoistureMaterial(models.Model):
    MATERIAL_CHOICES = (
        ("GRAVA", "Gravas"),
        ("FINO", "Finos"),
    )
    material            = models.CharField(choices=MATERIAL_CHOICES, max_length=6)
    bowl_weight         = models.FloatField()
    wet_weight          = models.FloatField()
    dry_weight          = models.FloatField()
    water_weight        = models.FloatField(editable=False)
    material_weight     = models.FloatField(editable=False)
    moisture            = models.FloatField(editable=False)
    moisture_content    = models.ForeignKey(MoistureContent, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate Water Weight
        water = self.wet_weight - self.dry_weight
        self.water_weight = round(water, 1)

        # Generate Material Weight
        material = self.dry_weight - self.bowl_weight
        self.material_weight = round(material, 1)

        # Generate Moisture
        moisture = self.water_weight/self.material_weight * 100
        self.moisture = round(moisture, 1)
        
        super(MoistureMaterial, self).save(*args, **kwargs)

    def __str__(self):
        return f"Humedad Material {self.id}"
