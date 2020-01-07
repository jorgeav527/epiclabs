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

class GranulometricGlobal(models.Model):
    SIZE_CHOICES = (
        ('4"', "4 inch"),
        ('3"', "3 inch"),
        ('2 1/2"', "2 1/2 inch"),
        ('2"', "2 inch"),
        ('1 1/2"', "1 1/2 inch"),
        ('1"', "1 inch"),
        ('3/4"', "3/4 inch"),
        ('1/2"', "1/2 inch"),
        ('3/8"', "3/8 inch"),
    )
    LAYER_CHOICES = (
        ("UNO", "Estrato 1"),
        ("DOS", "Estrato 2"),
        ("TRES", "Estrato 3"),
        ("CUATRO", "Estrato 4"),
    )
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Granulometria Tamizado Gloval")
    quarry          = models.CharField(max_length=50,)
    layer           = models.CharField(choices=LAYER_CHOICES, max_length=6)
    code            = models.CharField(max_length=255, unique=True, editable=False)
    sampling_date   = models.DateField()
    done_date       = models.DateField(default=datetime.datetime.now)
    dilate          = models.IntegerField(editable=False)
    hygr_humid      = models.FloatField(null=True, blank=True)
    organic         = models.BooleanField(default=False)
    liquid_limit    = models.FloatField()
    plastic_limit   = models.FloatField()
    plastic_index   = models.FloatField(editable=False)
    max_size        = models.CharField(choices=SIZE_CHOICES, max_length=7, default='2"')
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

        # Generate the plastic_index
        plastic = self.liquid_limit - self.plastic_limit
        self.plastic_index = round(plastic, 1)

        super(GranulometricGlobal, self).save(*args, **kwargs)

    def __str__(self):
        return f"Granulometria Tamizado Gloval {self.id}"


class GlobalMesh(models.Model):
    tamiz_4         = models.FloatField(null=True, blank=True)
    tamiz_3         = models.FloatField(null=True, blank=True)
    tamiz_2_1o2     = models.FloatField(null=True, blank=True)
    tamiz_2         = models.FloatField(null=True, blank=True)
    tamiz_1_1o2     = models.FloatField(null=True, blank=True)
    tamiz_1         = models.FloatField(null=True, blank=True)
    tamiz_3o4       = models.FloatField(null=True, blank=True)
    tamiz_1o2       = models.FloatField(null=True, blank=True)
    tamiz_3o8       = models.FloatField(null=True, blank=True)
    tamiz_N_4       = models.FloatField(null=True, blank=True)
    tamiz_N_8       = models.FloatField(null=True, blank=True)
    tamiz_N_10      = models.FloatField(null=True, blank=True)
    tamiz_N_16      = models.FloatField(null=True, blank=True)
    tamiz_N_20      = models.FloatField(null=True, blank=True)
    tamiz_N_30      = models.FloatField(null=True, blank=True)
    tamiz_N_40      = models.FloatField(null=True, blank=True)
    tamiz_N_50      = models.FloatField(null=True, blank=True)
    tamiz_N_60      = models.FloatField(null=True, blank=True)
    tamiz_N_80      = models.FloatField(null=True, blank=True)
    tamiz_N_100     = models.FloatField(null=True, blank=True)
    tamiz_N_140     = models.FloatField(null=True, blank=True)
    tamiz_N_200     = models.FloatField(null=True, blank=True)
    tamiz_fondo     = models.FloatField(null=True, blank=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    granulometric_global = models.ForeignKey(GranulometricGlobal, on_delete=models.CASCADE)
    equipment       = models.ManyToManyField(Equip)
    tool            = models.ManyToManyField(Tool)

    def __str__(self):
        return f"Tamizes {self.id}"
