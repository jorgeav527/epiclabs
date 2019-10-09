from django.db import models
import datetime
import math

from accounts.models import User
from equipments.models import Equip

# Create your models here.

class GroutDiceBreak(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, default="Rotura Dados Concreto")
    code            = models.CharField(max_length=255, unique=True, editable=False)
    fc_esp          = models.FloatField(default=280.00)
    fecha_vaciado   = models.DateField()
    fecha_rotura    = models.DateField(default=datetime.datetime.now)
    edad            = models.IntegerField(editable=False)
    largo_1         = models.FloatField(default=5.00)
    largo_2         = models.FloatField(default=5.00)
    ancho_1         = models.FloatField(default=5.00)
    ancho_2         = models.FloatField(default=5.00)
    area            = models.FloatField(editable=False)
    h               = models.FloatField(default=5.00)
    F               = models.FloatField()
    fc              = models.FloatField(editable=False)
    fc_175          = models.FloatField(editable=False)
    fc_210          = models.FloatField(editable=False)
    fc_280          = models.FloatField(editable=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    equipment       = models.ManyToManyField(Equip)

    def save(self, *args, **kwargs):
        # Generate the code for the barcode (e.g. RDC2009092701)
        date = datetime.datetime.today()
        letters = ""
        words = self.name.split()
        for word in words:
            letters += word[0]
        self.code = f"{letters.upper()}{date.year}{date.month}{date.day}{date.hour}{date.minute}{date.second}"

        # Generate the edad from the fecha_vaciado
        diff = self.fecha_rotura - self.fecha_vaciado
        self.edad = diff.days

        # Generate the area from the avg largo and ancho
        avg_largo = (self.largo_1 + self.largo_2)/2
        avg_ancho = (self.ancho_1 + self.ancho_2)/2
        self.area = round(avg_largo * avg_ancho, 2)
        
        # Generate the fc
        effort_fc = self.F/self.area
        self.fc = round(effort_fc, 2)

        # Generate the fc_175
        effort_fc_175 = (self.fc/175)*100 
        self.fc_175 = round(effort_fc_175, 2)

        # Generate the fc_210
        effort_fc_210 = (self.fc/210)*100 
        self.fc_210 = round(effort_fc_210, 2)

        # Generate the fc_280
        effort_fc_280 = (self.fc/280)*100 
        self.fc_280 = round(effort_fc_280, 2)

        super(GroutDiceBreak, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} {self.name} {self.code}"



