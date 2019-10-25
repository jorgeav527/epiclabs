from django import forms
from functools import partial
from datetime import datetime

from accounts.models import User
from tests_concrete.models import PiceBreak
from construction.models import Construction
from reference_person.models import ReferencePerson

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class PiceBreakForm(forms.ModelForm):
    DIAMETER_CHOICES = (
        (0, False),
        (2, "2 Inch"),
        (4, "4 Inch"),
        (6, "6 Inch"),
    )
    fc_esp          = forms.FloatField(required=True, initial=280.00, label="f'c epecificado", help_text="Unidades (kgf/cm²)",)
    poured_data     = forms.DateField(required=True, widget=DateInput(), label="Dia del Vaciado")
    break_data      = forms.DateField(required=True, initial=datetime.now(), widget=DateInput(), label="Dia de la Rotura")
    diameter_esp    = forms.ChoiceField(required=False, choices=DIAMETER_CHOICES, label="Diametro Especifico", help_text="Unidades (inch)",)
    diameter_1      = forms.FloatField(required=False, label="Diametro Superior", help_text="Unidades (inch)",)
    diameter_2      = forms.FloatField(required=False, label="Diametro Inferior", help_text="Unidades (inch)",)
    F               = forms.FloatField(required=True, label="Esfuerso Compresora", help_text="Unidades (kgf)",)

    class Meta:
        model = PiceBreak
        fields = [
            "fc_esp", 
            "poured_data", 
            "break_data", 
            "diameter_esp",
            "diameter_1",
            "diameter_2",
            "F",
        ]


class PiceBreakFormClient(forms.ModelForm):
    DIAMETER_CHOICES = (
        (0, False),
        (2, "2 Inch"),
        (4, "4 Inch"),
        (6, "6 Inch"),
    )
    user            = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), required=True, label="Escoje el Cliente" )
    fc_esp          = forms.FloatField(required=True, initial=280.00, label="f'c epecificado", help_text="Unidades (kgf/cm²)",)
    poured_data     = forms.DateField(required=True, widget=DateInput(), label="Dia del Vaciado")
    break_data      = forms.DateField(required=True, initial=datetime.now(), widget=DateInput(), label="Dia de la Rotura")
    diameter_esp    = forms.ChoiceField(required=False, choices=DIAMETER_CHOICES, label="Diametro Especifico", help_text="Unidades (inch)",)
    diameter_1      = forms.FloatField(required=False, label="Diametro Superior", help_text="Unidades (inch)",)
    diameter_2      = forms.FloatField(required=False, label="Diametro Inferior", help_text="Unidades (inch)",)
    F               = forms.FloatField(required=True, label="Esfuerso Compresora", help_text="Unidades (kgf)",)
    reference_person    = forms.ModelChoiceField(queryset=ReferencePerson.objects.filter(client_profile=1))
    construction        = forms.ModelChoiceField(queryset=Construction.objects.all())


    class Meta:
        model = PiceBreak
        fields = [
            "user",
            "fc_esp", 
            "poured_data", 
            "break_data", 
            "diameter_esp",
            "diameter_1",
            "diameter_2",
            "F",
            "reference_person",
            "construction",
        ]