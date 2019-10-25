from django import forms
from functools import partial
from datetime import datetime

from .models import Construction

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class ConstructionForm(forms.ModelForm):
    name          = forms.CharField(required=True, label="Nombre de la Construcción",)
    location      = forms.CharField(required=True, label="Lugar de la Construcción",)
    start_day     = forms.DateField(required=True, widget=DateInput(), label="Comienzo de la Obra")
    finish_day    = forms.DateField(required=True, widget=DateInput(), label="Fin de la Obra Aprox.")

    class Meta:
        model = Construction
        fields = ("name", "location", "start_day", "finish_day",)