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

class ProctorM(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Proctor Modificado")
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

        super(ProctorM, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Proctor Modificado {self.id}"


class DensityWetDry(models.Model):
    layers              = models.IntegerField(default=5)
    hits                = models.IntegerField()
    material_weight_P   = models.IntegerField()
    bowl_weight_P       = models.IntegerField(default=6380)
    compacted_weight_P  = models.IntegerField(editable=False)
    bowl_volume_P       = models.FloatField(default=2130.0)
    wet_density         = models.FloatField(editable=False)
    bowl                = models.IntegerField()
    bowl_weight         = models.FloatField()
    wet_weight          = models.FloatField()
    dry_weight          = models.FloatField()
    water_weight        = models.FloatField(editable=False)
    material_weight     = models.FloatField(editable=False)
    moisture            = models.FloatField(editable=False)
    dry_density         = models.FloatField(editable=False)
    proctor_m   = models.ForeignKey(ProctorM, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):
        # Generate de Compacted Weight
        self.compacted_weight_P = self.material_weight_P - self.bowl_weight_P

        # Generate Wet Density
        density_wet = self.compacted_weight_P / self.bowl_volume_P
        self.wet_density = round(density_wet, 3)

        # Generate Water Weight
        water = self.wet_weight - self.dry_weight
        self.water_weight = round(water, 1)

        # Generate Material Weight
        material = self.dry_weight - self.bowl_weight
        self.material_weight = round(material, 1)

        # Generate Moisture
        moisture = 100 * self.water_weight / self.material_weight
        self.moisture = round(moisture, 1)

        # Generate Dry Density
        density_dry = self.wet_density/(1+self.moisture/100)
        self.dry_density = round(density_dry, 2)

        super(DensityWetDry, self).save(*args, **kwargs)

    def __str__(self):
        return f"Densidad Seca y Humeda {self.id}"


class Saturation(models.Model):
    frac_extrad_weight  = models.FloatField()
    frac_gruesa_weight  = models.FloatField()       
    frac_fina_weight    = models.FloatField()       
    p_sp_frac_extrad    = models.FloatField()
    p_sp_frac_gruesa    = models.FloatField()
    g_sp_frac_fina      = models.FloatField()
    g_frac_fina_gruesa  = models.FloatField(editable=False)         
    g_sp_global         = models.FloatField(editable=False)
    proctor_m   = models.ForeignKey(ProctorM, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate Faction fina + gruesa
        fina_gruesa = 1/((((self.frac_gruesa_weight*100/(100-self.frac_extrad_weight))/100)/self.p_sp_frac_gruesa) + (((self.frac_fina_weight*100/(100-self.frac_extrad_weight))/100)/self.g_sp_frac_fina))
        self.g_frac_fina_gruesa = round(fina_gruesa, 3)

        # Generate Gr Sp Gloval
        sp_global = 1/((self.frac_extrad_weight/100/self.p_sp_frac_extrad)+(self.frac_gruesa_weight/100/self.p_sp_frac_gruesa)+(self.frac_fina_weight/100/self.g_sp_frac_fina))
        self.g_sp_global = round(sp_global, 3)

        super(Saturation, self).save(*args, **kwargs)

    def __str__(self):
        return f"Saturation {self.id}"


class Correction(models.Model):
    bowl_weight         = models.FloatField()
    wet_weight          = models.FloatField()
    dry_weight          = models.FloatField()
    water_weight        = models.FloatField(editable=False)
    material_weight     = models.FloatField(editable=False)
    moisture            = models.FloatField(editable=False)
    proctor_m   = models.ForeignKey(ProctorM, on_delete=models.CASCADE)
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
        
        super(Correction, self).save(*args, **kwargs)

    def __str__(self):
        return f"Correccion {self.id}"
