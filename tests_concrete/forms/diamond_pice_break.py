from django import forms
from functools import partial
from datetime import datetime

from accounts.models import User
from tests_concrete.models import DiamondPiceBreak
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class DiamondPiceBreakForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = DiamondPiceBreak
        fields = [
            'fc_esp',
            'element',
            'extraction_data', 
            'break_data', 
            'D',
            'L',
            'F',
            'course'
        ]
        labels = {
            'fc_esp': 'Resistencia de Diseño', 
            'element': 'Elemento',    
            'extraction_data': 'Dia de la Extracción', 
            'break_data': 'Dia de Rotura', 
            'D': 'Diametro',
            'L': 'Longitud',
            'F': 'Carga Maquina',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²)', 
            'D': 'Unidades (Pulgadas)',
            'L': 'Unidades (Pulgadas)',
            'F': 'Unidades (kgf)',
        }
        widgets = {
            'extraction_data': DateInput(),
            'break_data': DateInput(), 
        }
    
    def clean(self):
        cleaned_data = super().clean()
        D_passed = cleaned_data.get("D")
        L_passed = cleaned_data.get("L")
        if L_passed/D_passed > 1.75:
            raise forms.ValidationError("El factor L/D es mayor que 1.75 revisar Diametro y Longitud")


class DiamondPiceBreakFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoje el Cliente", required=True)

    class Meta:
        model = DiamondPiceBreak
        fields = [
            'user',
            'fc_esp',
            'element',
            'extraction_data', 
            'break_data', 
            'D',
            'L',
            'F',
            'reference_person',
            'construction',
        ]
        labels = {
            'fc_esp': 'Resistencia de Diseño', 
            'element': 'Elemento',    
            'extraction_data': 'Dia de la Extracción', 
            'break_data': 'Dia de Rotura', 
            'D': 'Diametro',
            'L': 'Longitud',
            'F': 'Carga Maquina',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²)', 
            'D': 'Unidades (Pulgadas)',
            'L': 'Unidades (Pulgadas)',
            'F': 'Unidades (kgf)',
        }
        widgets = {
            'extraction_data': DateInput(),
            'break_data': DateInput(), 
        }

    def clean(self):
        cleaned_data = super().clean()
        D_passed = cleaned_data.get("D")
        L_passed = cleaned_data.get("L")
        if L_passed/D_passed > 1.75:
            raise forms.ValidationError("El factor L/D es mayor que 1.75 revisar Diametro y Longitud")

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