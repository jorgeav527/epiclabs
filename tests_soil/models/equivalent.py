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

class Equivalent(models.Model):
    LAYER_CHOICES = (
        ("UNO", "Estrato 1"),
        ("DOS", "Estrato 2"),
        ("TRES", "Estrato 3"),
        ("CUATRO", "Estrato 4"),
    )
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Valor Equivalente Arena Finos")
    pit             = models.CharField(max_length=50, null=True, blank=True)
    layer           = models.CharField(choices=LAYER_CHOICES, max_length=6)
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

        super(Equivalent, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Valor Equivalente Arena Finos {self.id}"


class Equiv(models.Model):
    max_size        = models.FloatField(default=4.75)
    start_sat_time  = models.TimeField(default=datetime.time(00,00)) 
    out_sat_time    = models.TimeField(default=datetime.time(00,00))
    start_dec_time  = models.TimeField(default=datetime.time(00,00))
    out_dec_time    = models.TimeField(default=datetime.time(00,00))
    max_high_fine   = models.FloatField()
    max_high_sand   = models.FloatField()
    equiv_sand      = models.FloatField(editable=False)
    equivalent  = models.ForeignKey(Equivalent, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):
        equiv_sand = self.max_high_sand / self.max_high_fine * 100.0
        self.equiv_sand = math.ceil(equiv_sand)
        
        super(Equiv, self).save(*args, **kwargs)

    def __str__(self):
        return f"Equiv {self.id}"
