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

class SandCone(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    name                = models.CharField(max_length=50, default="Sand Cone")
    sampling_name       = models.CharField(max_length=50,)
    progressive_sector  = models.CharField(max_length=50, null=True, blank=True)
    section_level       = models.CharField(max_length=50, null=True, blank=True)
    element_side        = models.CharField(max_length=50, null=True, blank=True)
    layer               = models.CharField(max_length=50, null=True, blank=True)
    weight_dry_max      = models.FloatField(null=True, blank=True)
    opt_moisture        = models.FloatField(null=True, blank=True)    
    moisture            = models.BooleanField(default=False)
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

        super(SandCone, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Sand Cone {self.id}"


class HumidDensity(models.Model):
    bowl_weight_sand            = models.IntegerField()
    bowl_weight_remaining_sand  = models.IntegerField()
    weight_sand                 = models.IntegerField(editable=False)
    weight_sand_cone_plate      = models.IntegerField()
    weight_sand_excavation      = models.IntegerField(editable=False)
    sand_density                = models.FloatField()
    volume_material_extracted   = models.FloatField(editable=False)
    sample_weight_container     = models.IntegerField()
    container_weight            = models.IntegerField(default=0)
    wet_sample_weight           = models.IntegerField(editable=False)
    density_wet_sample          = models.FloatField(editable=False)
    sand_cone   = models.ForeignKey(SandCone, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

 
    def save(self, *args, **kwargs):
        # Generate  Weight Sand
        w_s = self.bowl_weight_sand - self.bowl_weight_remaining_sand
        self.weight_sand = w_s

        # Generate Weight Sand Excavation
        w_s_e = self.weight_sand - self.weight_sand_cone_plate
        self.weight_sand_excavation = w_s_e   

        # Generate Volume Material Extracted
        v_m_e = self.weight_sand_excavation / self.sand_density
        self.volume_material_extracted = round(v_m_e, 2)

        # Generate Wet Sample Weight
        w_s_w = self.sample_weight_container - self.container_weight
        self.wet_sample_weight = w_s_w

        # Generate Density Wet Sample
        d_w_s = self.wet_sample_weight / self.volume_material_extracted
        self.density_wet_sample = round(d_w_s, 2)

        super(HumidDensity, self).save(*args, **kwargs)

    def __str__(self):
        return f"Densidad Humeda {self.id}"


class ContentMoisture(models.Model):
    sample_fraction_pass    = models.CharField(max_length=15, default='Pas. 3/4"')
    bowl_weight             = models.FloatField()
    wet_sample_weight_bowl  = models.FloatField()
    dry_sample_weight_bowl  = models.FloatField()
    weight_water            = models.FloatField(editable=False)
    dry_sample_weight       = models.FloatField(editable=False)
    sample_moisture         = models.FloatField(editable=False)
    sand_cone   = models.ForeignKey(SandCone, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):
        # Generate the weight water
        w_w = self.wet_sample_weight_bowl - self.dry_sample_weight_bowl
        self.weight_water = round(w_w, 1)

        # Generate the dry sample weight
        d_s_w = self.dry_sample_weight_bowl - self.bowl_weight
        self.dry_sample_weight = round(d_s_w, 1)

        # Generate the mosture %
        s_m = self.weight_water / self.dry_sample_weight * 100
        self.sample_moisture = round(s_m, 1)

        super(ContentMoisture, self).save(*args, **kwargs)

    def __str__(self):
        return f"Contenido Humedad {self.id}"



class CorrectionSandCone(models.Model):
    wet_fraction_weight     = models.IntegerField()
    p_e_ap_frac_extrad      = models.FloatField()
    per_abs_tails_extrad    = models.FloatField()
    weight_fraction_extrad  = models.FloatField(editable=False)
    sand_cone   = models.ForeignKey(SandCone, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool) 

    def save(self, *args, **kwargs):
        # Generate the weight fraction extrad
        w_f_e = self.wet_fraction_weight / (1 + (self.per_abs_tails_extrad / 100))
        self.weight_fraction_extrad = round(w_f_e, 2)

        super(CorrectionSandCone, self).save(*args, **kwargs)

    def __str__(self):
        return f"Correccion Sand Cone {self.id}"