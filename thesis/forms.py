from django import forms
from functools import partial
from datetime import datetime

from .models import Thesis
from course.models import Course
from accounts.models import TeacherProfile

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class ThesisForm(forms.ModelForm):
    LINE_CHOICES = (
        ("NINGUNA", "Ninguna"),
        ("AGREGADOS", "Agregados"),
        ("GEOTECNIA", "Geotecnia"),
        ("MECANICA_DE_MATERIALES", "Mecánica de Materiales"),
        ("TECNOLOGIAS_MODERNAS", "Tecnologías Modernas"),
    )

    title           = forms.CharField(required=True, label="Titulo de la Tesis")
    line            = forms.ChoiceField(choices=LINE_CHOICES, required=True, label="Linea de Desarrollo")
    course          = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), required=True, label="Cursos afin a la Tesis")
    adviser         = forms.ModelMultipleChoiceField(queryset=TeacherProfile.objects.all(), required=True, label="Seleccionar Acesores")
    start_day       = forms.DateField(required=True, initial=datetime.now(), widget=DateInput(), label="Comienzo de la Tesis")
    finish_day      = forms.DateField(required=True, widget=DateInput(), label="Fin de la Tesis")

    class Meta:
        model = Thesis
        fields = ("title", "line", "course", "adviser", "start_day", "finish_day",)