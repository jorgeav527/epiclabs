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

class BrickType(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Tipo Ladrillo")
    name_element    = models.CharField(max_length=50, null=True, blank=True)
    brick_company   = models.CharField(max_length=100, null=True, blank=True)
    n_d_length      = models.FloatField()
    n_d_width       = models.FloatField()
    n_d_high        = models.FloatField()
    code            = models.CharField(max_length=255, unique=True, editable=False)
    sampling_date   = models.DateField()
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

        super(BrickType, self).save(*args, **kwargs)

    def __str__(self):
        return f"Tipo Ladrillo {self.id}"


class VariationDimensions(models.Model):
    upface_length   = models.FloatField()
    downface_length = models.FloatField()
    average_length  = models.FloatField(editable=False)
    upface_width    = models.FloatField()
    downface_width  = models.FloatField()
    average_width   = models.FloatField(editable=False)
    high_backside   = models.FloatField()
    high_rightside  = models.FloatField()
    high_frontside  = models.FloatField()
    high_lefside    = models.FloatField()
    average_high    = models.FloatField(editable=False)
    brick_type  = models.ForeignKey(BrickType, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate average_length
        al = (self.upface_length + self.downface_length) / 2
        self.average_length = round(al, 2)

        # Generate average_width
        aw = (self.upface_width + self.downface_width) / 2
        self.average_width = round(aw, 2)

        # Generate average_high
        ah = (self.high_backside + self.high_rightside + self.high_frontside + self.high_lefside) / 4
        self.average_high = round(ah, 2)

        super(VariationDimensions, self).save(*args, **kwargs)

    def __str__(self):
        return f"Variacion Dimenciones Ladrillo {self.id}"


class Warping(models.Model):
    upface_concave      = models.FloatField(default=0)
    upface_convex       = models.FloatField(default=0)
    downface_concave    = models.FloatField(default=0)
    downface_convex     = models.FloatField(default=0)
    brick_type  = models.ForeignKey(BrickType, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def __str__(self):
        return f"Alabeo Ladrillo {self.id}"


class DensityVoids(models.Model):
    length          = models.FloatField()
    width           = models.FloatField()
    high            = models.FloatField()
    volume_brick    = models.FloatField(editable=False)
    sc              = models.FloatField()
    su              = models.FloatField()
    volume_void     = models.FloatField(editable=False)
    volume_real     = models.FloatField(editable=False)
    void_percentage = models.FloatField(editable=False)
    weight          = models.FloatField()
    density         = models.FloatField(editable=False)
    brick_type  = models.ForeignKey(BrickType, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate volume_brick
        volume = self.length * self.width * self.high
        self.volume_brick = round(volume, 2)

        # Generate volume_void
        vv = ( 500 / self.sc ) * self.su
        self.volume_void = round(vv, 2)

        # Generate volume_real
        vr = self.volume_brick - self.volume_void
        self.volume_real = round(vr, 2)

        # Generate void_percentage
        vp = (self.volume_void / self.volume_brick) * (1/1.64) * 100
        self.void_percentage = round(vp, 0)

        # Generate density
        d = self.weight / self.volume_real
        self.density = round(d, 2)

        super(DensityVoids, self).save(*args, **kwargs)

    def __str__(self):
        return f"Densidad y Vacios {self.id}"


class Suction(models.Model):
    nomal_weight    = models.FloatField()
    dry_weight      = models.FloatField()
    diff_weight     = models.FloatField(editable=False)
    length          = models.FloatField()
    width           = models.FloatField()
    face_area       = models.FloatField(editable=False)
    face_wet_weight = models.FloatField()
    face_wet_weight_correction = models.FloatField(editable=False)
    brick_type  = models.ForeignKey(BrickType, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate diff_weight
        dw = self.nomal_weight - self.dry_weight
        self.diff_weight = round(dw, 2)

        # Generate face_area
        fa = self.length * self.width
        self.face_area = round(fa, 2)

        # Generate face_wet_weight_correction
        if self.face_area > (200 + (200 * 2.5 / 100)) or self.face_area < (200 - (200 * 2.5 / 100)):
            fwwc = (200 * self.face_wet_weight) / (self.length * self.width)
            self.face_wet_weight_correction = round(fwwc, 2)
        else:
            self.face_wet_weight_correction = round(self.face_wet_weight, 2) 

        super(Suction, self).save(*args, **kwargs)

    def __str__(self):
        return f"Succion Ladrillo {self.id}"


class AbsSatuCoeff(models.Model):
    dry_weight          = models.FloatField()
    wet_weight_cool_24  = models.FloatField()
    wet_weight_hot_5    = models.FloatField()
    abs_brick           = models.FloatField(editable=False)
    abs_max_brick       = models.FloatField(editable=False)
    coeff_sat           = models.FloatField(editable=False)
    brick_type  = models.ForeignKey(BrickType, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate abs_brick
        ab = 100 * (self.wet_weight_cool_24 - self.dry_weight) / self.dry_weight
        self.abs_brick = round(ab, 1)

        # Generate abs_max_brick
        amb = 100 * (self.wet_weight_hot_5 - self.dry_weight) / self.dry_weight
        self.abs_max_brick = round(amb, 1)
        
        # Generate coeff_sat
        cs = (self.wet_weight_cool_24 - self.dry_weight) / (self.wet_weight_hot_5 - self.dry_weight)
        self.coeff_sat = round(cs, 3)

        super(AbsSatuCoeff, self).save(*args, **kwargs)

    def __str__(self):
        return f"Absorcion Coeficiente Saturacion Ladrillo {self.id}"


class CompretionBrick(models.Model):
    upface_length   = models.FloatField()
    upface_width    = models.FloatField()
    downface_length = models.FloatField()
    downface_width  = models.FloatField()
    upface_area     = models.FloatField(editable=False)
    downface_area   = models.FloatField(editable=False)
    average_area    = models.FloatField(editable=False)
    load            = models.FloatField()
    fc              = models.FloatField(editable=False)
    fc_MPa          = models.FloatField(editable=False)
    brick_type  = models.ForeignKey(BrickType, on_delete=models.CASCADE)
    equipment   = models.ManyToManyField(Equip)
    tool        = models.ManyToManyField(Tool)    

    def save(self, *args, **kwargs):

        # Generate upface_area
        afa = self.upface_length * self.upface_width 
        self.upface_area = round(afa, 2)

        # Generate downface_area
        dfa = self.downface_length * self.downface_width 
        self.downface_area = round(dfa, 2)
        
        # Generate average_area
        aa = (self.upface_area + self.downface_area) / 2
        self.average_area = round(aa, 2)

        # Generate compression_resistance
        fc = self.load / self.average_area
        self.fc = round(fc, 2)

        # Generate fc_MPa
        fc_MPa = self.fc*0.0981 
        self.fc_MPa = round(fc_MPa, 2)

        super(CompretionBrick, self).save(*args, **kwargs)

    def __str__(self):
        return f"Compresion Ladrillo {self.id}"
