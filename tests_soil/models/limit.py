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

class Limit(models.Model):
    LAYER_CHOICES = (
        ("UNO", "Estrato 1"),
        ("DOS", "Estrato 2"),
        ("TRES", "Estrato 3"),
        ("CUATRO", "Estrato 4"),
    )
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Límite Líquido Pastico")
    pit             = models.CharField(max_length=50, null=True, blank=True)
    layer           = models.CharField(choices=LAYER_CHOICES, max_length=6)
    code            = models.CharField(max_length=255, unique=True, editable=False)
    extraction_data = models.DateField()
    done_data       = models.DateField(default=datetime.datetime.now)
    duration        = models.IntegerField(editable=False)
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
        diff = self.done_data - self.extraction_data
        self.duration = diff.days

        super(Limit, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Límite Líquido Plástico {self.id}"


class Liquid(models.Model):
    bowl        = models.IntegerField()
    hit         = models.IntegerField()
    bowl_weight = models.FloatField()
    wet_weight  = models.FloatField()
    dry_weight  = models.FloatField()
    water_weight    = models.FloatField(editable=False)
    material_weight = models.FloatField(editable=False)
    moisture    = models.FloatField(editable=False)
    limit       = models.ForeignKey(Limit, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    


    def save(self, *args, **kwargs):
        # Generate the water weight of the material
        water = self.wet_weight - self.dry_weight
        self.water_weight = round(water, 2)

        # Generate the material weight
        material_dry = self.dry_weight - self.bowl_weight
        self.material_weight = round(material_dry, 2)

        # Generate the mosture %
        moisture = (self.water_weight / self.material_weight) * 100
        self.moisture = round(moisture, 1)

        super(Liquid, self).save(*args, **kwargs)

    def __str__(self):
        return f"Límite Líquido {self.id}"


class Platic(models.Model):
    bowl        = models.IntegerField()
    bowl_weight = models.FloatField()
    wet_weight  = models.FloatField()
    dry_weight  = models.FloatField()
    water_weight    = models.FloatField(editable=False)
    material_weight = models.FloatField(editable=False)
    moisture    = models.FloatField(editable=False)
    limit       = models.ForeignKey(Limit, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    


    def save(self, *args, **kwargs):
        # Generate the water weight of the material
        water = self.wet_weight - self.dry_weight
        self.water_weight = round(water, 2)

        # Generate the material weight
        material_dry = self.dry_weight - self.bowl_weight
        self.material_weight = round(material_dry, 2)

        # Generate the mosture %
        moisture = (self.water_weight / self.material_weight) * 100
        self.moisture = round(moisture, 1)

        super(Platic, self).save(*args, **kwargs)

    def __str__(self):
        return f"Límite Plástico {self.id}"
