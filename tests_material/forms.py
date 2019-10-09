from django import forms
from functools import partial
from datetime import datetime
from django.conf import settings

from .models import GroutDiceBreak

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class GroutDiceBreakForm(forms.ModelForm):
    fecha_rotura = forms.DateField(
        initial=datetime.now(),
        widget=DateInput()
    )
    fecha_vaciado = forms.DateField(
        widget=DateInput()
    )

    class Meta:
        model = GroutDiceBreak
        fields = [
            "name", 
            "fc_esp", 
            "fecha_vaciado", 
            "fecha_rotura", 
            "largo_1", 
            "largo_2", 
            "ancho_1", 
            "ancho_2", 
            "h",
            "F",
        ]


