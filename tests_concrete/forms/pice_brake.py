from django import forms
from functools import partial
from datetime import datetime
from django.conf import settings

from accounts.models import User
from tests_concrete.models import PiceBreak

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class PiceBreakForm(forms.ModelForm):
    fecha_rotura = forms.DateField(
        initial=datetime.now(),
        widget=DateInput()
    )
    fecha_vaciado = forms.DateField(
        widget=DateInput()
    )

    class Meta:
        model = PiceBreak
        fields = [
            "fc_esp", 
            "fecha_vaciado", 
            "fecha_rotura", 
            "diameter_esp",
            "diameter_1",
            "diameter_2",
            "h",
            "F",
        ]


class PiceBreakFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_client=True)
    )

    fecha_rotura = forms.DateField(
        initial=datetime.now(),
        widget=DateInput()
    )
    fecha_vaciado = forms.DateField(
        widget=DateInput()
    )

    class Meta:
        model = PiceBreak
        fields = [
            "user",
            "fc_esp", 
            "fecha_vaciado", 
            "fecha_rotura", 
            "diameter_esp",
            "diameter_1",
            "diameter_2",
            "h",
            "F",
        ]