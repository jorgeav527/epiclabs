from django import forms
from functools import partial
from datetime import datetime

from accounts.models import User
from tests_concrete.models import LimeDiceBreak
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class LimeDiceBreakForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = LimeDiceBreak
        fields = [
            'fc_esp',
            'element', 
            'poured_data', 
            'break_data', 
            'd_1',
            'd_2',
            'F',
            'course'
        ]
        labels = {
            'fc_esp': 'Resistencia de Diseño', 
            'element': 'Elemento',    
            'poured_data': 'Dia de Vaciado', 
            'break_data': 'Dia de Rotura', 
            'd_1': 'Longitud',
            'd_2': 'Ancho',
            'F': 'Carga Maquina',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²)', 
            'd_1': 'Unidades (Centimetros)',
            'd_2': 'Unidades (Centimetros)',
            'F': 'Unidades (kgf)',
        }
        widgets = {
            'poured_data': DateInput(),
            'break_data': DateInput(), 
        }



class LimeDiceBreakFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoje el Cliente", required=True)

    class Meta:
        model = LimeDiceBreak
        fields = [
            'user',
            'fc_esp', 
            'element', 
            'poured_data', 
            'break_data', 
            'd_1',
            'd_2',
            'F',
            'reference_person',
            'construction',
        ]
        labels = {
            'fc_esp': 'Resistencia de Diseño', 
            'element': 'Elemento',    
            'poured_data': 'Dia de Vaciado', 
            'break_data': 'Dia de Rotura', 
            'd_1': 'Longitud',
            'd_2': 'Ancho',
            'F': 'Carga Maquina',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²)', 
            'd_1': 'Unidades (Pulgadas)',
            'd_2': 'Unidades (Pulgadas)',
            'F': 'Unidades (kgf)',
        }
        widgets = {
            'poured_data': DateInput(),
            'break_data': DateInput(), 
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