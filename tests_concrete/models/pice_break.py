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


class PiceBreak(models.Model):
    COMPOSITION_CHOICES = (
        ("CONCRETO", "Testigo de Concreto"),
        ("CAL", "Testigo de Cal"),
    )
    pice_type       = models.CharField(max_length=10, choices=COMPOSITION_CHOICES, default="CONCRETO", db_column='Tipo de Testigo')
    user            = models.ForeignKey(User, on_delete=models.CASCADE, db_column='Usuario')
    sampling_date   = models.DateField(default=datetime.datetime.now, null=True, blank=True, db_column='Fecha de Muestreo')
    name            = models.CharField(max_length=50, default="Rotura Testigo", db_column='Nombre Propio')
    code            = models.CharField(max_length=255, unique=True, editable=False, db_column='Codigo')
    fc_esp          = models.FloatField(default=280, db_column='Esfuerzo Especificado')
    created         = models.DateTimeField(auto_now_add=True, db_column='Creado')
    updated         = models.DateTimeField(auto_now=True, db_column='Actualizado')
    equipment           = models.ManyToManyField(Equip, db_column='Equipos', db_table='Ensayo de Testigos - Uso de Equipos')
    tool                = models.ManyToManyField(Tool, db_column='Herramientas', db_table='Ensayo de Testigos - Uso de Herramientas')    
    course              = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, db_column='Curso')
    reference_person    = models.ForeignKey(ReferencePerson, on_delete=models.SET_NULL, null=True, blank=True, db_column='Persona de Referencia')
    construction        = models.ForeignKey(Construction, on_delete=models.SET_NULL, null=True, blank=True, db_column='Construccion')

    class Meta:
        db_table = 'Ensayos de Testigos'

    def save(self, *args, **kwargs):
        # Generate the code for the barcode (e.g. RDC2009092701)
        date = datetime.datetime.today()
        letters = ""
        words = self.name.split()
        for word in words:
            letters += word[0]
        self.code = f"{letters.upper()}{date.year}{date.month}{date.day}{date.hour}{date.minute}{date.second}"

        super(PiceBreak, self).save(*args, **kwargs)

    def __str__(self):
        return f"Testigo {self.id}"


class Pice(models.Model):
    poured_date     = models.DateField(db_column='Fecha de Vaciado')
    break_date      = models.DateField(db_column='Fecha de Rotura')
    dilate          = models.IntegerField(editable=False, db_column='Diferencia entre Fechas')
    element_name    = models.CharField(max_length=100, null=True, blank=True, db_column='Nombre del Elemento')
    D_1             = models.FloatField(db_column='Diametro 1')
    D_2             = models.FloatField(db_column='Diametro 2')
    area            = models.FloatField(editable=False, db_column='Area')
    load            = models.FloatField(db_column='Carga')
    fc              = models.FloatField(editable=False, db_column='Esfuerzo')
    fc_MPa          = models.FloatField(editable=False, db_column='Esfuerzo MPa')
    fc_175          = models.FloatField(editable=False, db_column='Esfuerzo a 175')
    fc_210          = models.FloatField(editable=False, db_column='Esfuerzo a 210')
    fc_280          = models.FloatField(editable=False, db_column='Esfuerzo a 280')
    created         = models.DateTimeField(auto_now_add=True, db_column='Creado')
    updated         = models.DateTimeField(auto_now=True, db_column='Actualizado')
    pice_break      = models.ForeignKey(PiceBreak, on_delete=models.CASCADE, db_column='Ensayos de Testigos')
    equipment       = models.ManyToManyField(Equip, db_column='Equipos', db_table='Testigos - Uso de Equipos')
    tool            = models.ManyToManyField(Tool, db_column='Herramientas', db_table='Testigos - Uso de Herramientas')

    class Meta:
        db_table = 'Testigos'

    def save(self, *args, **kwargs):
        # Generate the dilate from the poured_date
        diff = self.break_date - self.poured_date
        self.dilate = diff.days

        # Generate the area
        avg_D = ((self.D_1 + self.D_2) / 2) * 2.54
        area_cm2 = ((avg_D**2)*math.pi) / 4
        self.area = round(area_cm2, 2)

        # Generate the fc
        effort_fc = self.load / self.area
        self.fc = round(effort_fc, 2)

        # Generate fc_MPa
        effort_fc_MPa = self.fc * 0.0981 
        self.fc_MPa = round(effort_fc_MPa, 2)

        # Generate the fc_175
        effort_fc_175 = (self.fc / 175) * 100 
        self.fc_175 = round(effort_fc_175, 2)

        # Generate the fc_210
        effort_fc_210 = (self.fc / 210) * 100 
        self.fc_210 = round(effort_fc_210, 2)

        # Generate the fc_280
        effort_fc_280 = (self.fc / 280) * 100 
        self.fc_280 = round(effort_fc_280, 2)

        super(Pice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Testigos {self.id}"
