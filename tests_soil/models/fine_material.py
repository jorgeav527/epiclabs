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

class FineMaterial(models.Model):
    LAYER_CHOICES = (
        ("UNO", "Estrato 1"),
        ("DOS", "Estrato 2"),
        ("TRES", "Estrato 3"),
        ("CUATRO", "Estrato 4"),
    )
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Material Mas Fino")
    pit             = models.CharField(max_length=50, null=True, blank=True)
    layer           = models.CharField(choices=LAYER_CHOICES, max_length=6)
    code            = models.CharField(max_length=255, unique=True, editable=False)
    sampling_date   = models.DateField()
    done_date       = models.DateField(default=datetime.datetime.now)
    duration        = models.IntegerField(editable=False)
    bowl            = models.IntegerField()
    before_weight   = models.FloatField()
    bowl_weight     = models.FloatField()
    dry_weight      = models.FloatField()
    after_weight    = models.FloatField(editable=False)
    pass_weight     = models.FloatField(editable=False)
    fine            = models.FloatField(editable=False)
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

        # Generate the dilate from the sampling date
        diff = self.done_date - self.sampling_date
        self.duration = diff.days

        # Generate the material weight
        material_dry = self.dry_weight - self.bowl_weight
        self.after_weight = round(material_dry, 2)

        # Generate the pass material weight
        material_pass = self.before_weight - self.after_weight
        self.pass_weight = round(material_pass, 2)

        # Generate the mosture %
        material_fine = (self.pass_weight / self.before_weight) * 100
        self.fine = round(material_fine, 2)

        super(FineMaterial, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Material Mas Fino {self.id}"

