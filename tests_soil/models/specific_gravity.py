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

class SpecificGravity(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Gravedad Especifica")
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

        super(SpecificGravity, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Gravedad Especifica {self.id}"


class FractionPass(models.Model):
    material_pass           = models.FloatField()
    temperature             = models.FloatField(default=21.0)
    water_density           = models.FloatField(default=0.99799)
    pycnometer_volume       = models.FloatField()
    pycnometer_mass         = models.FloatField()
    mass_pycnometer_water   = models.FloatField(editable=False)
    sample_mass             = models.FloatField()
    mass_pyc_w_sample       = models.FloatField()
    mass_bowl               = models.FloatField()
    mass_bowl_sample        = models.FloatField()
    mass_dry_sample         = models.FloatField(editable=False)
    gravity_specific        = models.FloatField(editable=False)
    coefficient_water       = models.FloatField(default=0.99979)
    gravity_specific_real   = models.FloatField(editable=False)                 
    specific_gravity    = models.ForeignKey(SpecificGravity, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate the Mass of the Pycometer + water
        pycnometer_water = self.pycnometer_mass + (self.pycnometer_volume * self.water_density)
        self.mass_pycnometer_water = round(pycnometer_water, 2)

        # Generate the Mass of the dry sample
        dry_sample = self.mass_bowl_sample - self.mass_bowl
        self.mass_dry_sample = round(dry_sample, 2)
        
        # Generate the Gravity Specific
        gr_sp = self.mass_dry_sample / (self.mass_pycnometer_water - (self.mass_pyc_w_sample - self.mass_dry_sample))
        self.gravity_specific = round(gr_sp, 3)

        # Generate the Real Gravity Specific
        gr_sp_real = self.gravity_specific * self.coefficient_water
        self.gravity_specific_real = round(gr_sp_real, 3)

        super(FractionPass, self).save(*args, **kwargs)

    def __str__(self):
        return f"Fraccion Pasante {self.id}"


class FractionRetained(models.Model):
    material_retained       = models.FloatField()
    temperature_23          = models.FloatField(default=22.0)
    saturated_sample        = models.FloatField()
    w_basket_water          = models.FloatField()
    w_basket_water_sample   = models.FloatField()
    w_bowl                  = models.FloatField()
    w_bowl_sample           = models.FloatField() 
    w_sample_dry            = models.FloatField(editable=False)
    w_sample_sat_water      = models.FloatField(editable=False)
    specific_grav_mass      = models.FloatField(editable=False)
    specific_grav_mass_sss  = models.FloatField(editable=False)
    apparent_spe_gravity    = models.FloatField(editable=False)
    coefficient_water       = models.FloatField(default=0.99979)
    specific_mass_weight    = models.FloatField(editable=False)
    specific_mass_weight_sss = models.FloatField(editable=False)
    specific_mass_weight_app = models.FloatField(editable=False)
    absorption              = models.FloatField(editable=False)
    specific_gravity    = models.ForeignKey(SpecificGravity, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate the Mass of the dry sample
        dry_sample = self.w_bowl_sample - self.w_bowl
        self.w_sample_dry = round(dry_sample, 1)

        # Generate Weight Sample Sat in the Water
        sample_sat_water = self.w_basket_water_sample - self.w_basket_water
        self.w_sample_sat_water = round(sample_sat_water, 1)

        # Generate Specific gravity of Mass
        sp_gr = self.w_sample_dry / (self.saturated_sample - self.w_sample_sat_water)
        self.specific_grav_mass = round(sp_gr, 3)

        # Generate Specific gravity of SSS mass
        sp_gr_sss = self.saturated_sample / (self.saturated_sample - self.w_sample_sat_water)
        self.specific_grav_mass_sss = round(sp_gr_sss, 3)

        # Generate apparent specific gravity
        ap_sp_gr = self.w_sample_dry / (self.w_sample_dry - self.w_sample_sat_water)
        self.apparent_spe_gravity = round(ap_sp_gr, 3)

        # Generate Specific Mass Weight
        smw = self.coefficient_water * self.specific_grav_mass
        self.specific_mass_weight = round(smw, 3)

        # Generate Specific Mass Weight SSS
        smw_sss = self.coefficient_water * self.specific_grav_mass_sss
        self.specific_mass_weight_sss = round(smw_sss, 3)

        # Generate Specific Mass Weight Apparent
        smw_app = self.coefficient_water * self.apparent_spe_gravity
        self.specific_mass_weight_app = round(smw_app, 3)

        # Generate absorption
        abs_generate = (self.saturated_sample - self.w_sample_dry) / self.w_sample_dry * 100
        self.absorption = round(abs_generate, 1) 

        super(FractionRetained, self).save(*args, **kwargs)

    def __str__(self):
        return f"Fraccion Retenida {self.id}"

