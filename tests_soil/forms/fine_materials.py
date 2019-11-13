from django import forms
from functools import partial
from datetime import datetime

from accounts.models import User
from tests_soil.models import FineMaterial
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class FineMaterialForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = FineMaterial
        fields = [
            'pit',
            'layer',
            'sampling_date',
            'done_date',
            'bowl',
            'before_weight',
            'bowl_weight',
            'dry_weight',
            'course'
        ]
        labels = {
            'pit': 'Calicata',
            'layer': 'Estrato',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'bowl': 'Recipiente',
            'before_weight': 'Peso de muestra seca antes del lavado',
            'bowl_weight': 'Peso del recipiente',
            'dry_weight': 'Peso de suelo seco al horno',
        }
        help_texts = {
            'pit': 'Nombre Propio de la Calicata',
            'bowl': 'Numero del Recipiente',
            'before_weight': 'Unidades (gramos)',
            'bowl_weight': 'Unidades (gramos)',
            'dry_weight': '+ Recipiente,',
            'dry_weight': 'Unidades (gramos)',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class FineMaterialFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoje el Cliente", required=True)

    class Meta:
        model = FineMaterial
        fields = [
            'user',
            'pit',
            'layer',
            'sampling_date',
            'done_date',
            'bowl',
            'before_weight',
            'bowl_weight',
            'dry_weight',
            'reference_person',
            'construction',
        ]
        labels = {
            'pit': 'Calicata',
            'layer': 'Estrato',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'bowl': 'Recipiente',
            'before_weight': 'Peso de muestra seca antes del lavado',
            'bowl_weight': 'Peso del recipiente',
            'dry_weight': 'Peso de suelo seco al horno',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'pit': 'Nombre Propio de la Calicata',
            'bowl': 'Numero del Recipiente',
            'before_weight': 'Unidades (gramos)',
            'bowl_weight': 'Unidades (gramos)',
            'dry_weight': 'Unidades (gramos) + Peso del Recipiente',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reference_person'].queryset = ReferencePerson.objects.none()
        self.fields['reference_person'].required = True
        self.fields['construction'].queryset = Construction.objects.none()
        self.fields['construction'].required = True

        if 'user' in self.data:
            try:
                user_id = int(self.data.get('user'))
                self.fields['reference_person'].queryset = ReferencePerson.objects.filter(client_profile__user=user_id)
                self.fields['construction'].queryset = Construction.objects.filter(client_profile__user=user_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

        elif self.instance.pk:
            self.fields['reference_person'].queryset = self.instance.user.clientprofile.referenceperson_set.all()
            self.fields['reference_person'].required = True
            self.fields['construction'].queryset = self.instance.user.clientprofile.construction_set.all()
            self.fields['construction'].required = True


