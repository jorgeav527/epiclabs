from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_concrete.models import DiamondPiceBreak, DiamondPice
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
            'course'
        ]
        labels = {
            'fc_esp': 'Resistencia de Diseño', 
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²) <br> Aproximación (1 kgf/cm²)', 
        }
    

class DiamondPiceBreakFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)
    sampling_date = forms.DateField(required=True, label="Fecha de Muestreo", widget=DateInput(), initial=datetime.now)

    class Meta:
        model = DiamondPiceBreak
        fields = [
            'user',
            'fc_esp',
            'sampling_date', 
            'reference_person',
            'construction',
        ]
        labels = {
            'fc_esp': 'Resistencia de Diseño', 
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²) <br> Aproximación (1 kgf/cm²)', 
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


class DiamondPiceForm(forms.ModelForm):

    class Meta:
        model = DiamondPice
        fields = [
            'extraction_date',
            'break_date',
            'element_name',
            'D',
            'L',
            'check_per',
            'load',
        ]
        labels = {
            'extraction_date': 'Fecha de Extracción',
            'break_date': 'Fecha de Rotura',
            'element_name': 'Elemento',    
            'D': 'Diámetro',
            'L': 'Longitud',
            'check_per': 'Verificación de la Perpendicularidad',
            'load': 'Carga',
        }
        help_texts = {
            'extraction_date': 'mm/dd/yyyy',
            'break_date': 'mm/dd/yyyy',
            'D': 'Unidades (mm) <br> Aproximación (1 mm)',
            'L': 'Unidades (mm) <br> Aproximación (1 mm)',
            'load': 'Unidades (kgf) <br> Aproximación (1 kgf)',
        }
        widgets = {
            'extraction_date': DateInput(),
            'break_date': DateInput(),
        }

DiamondPiceFormSet = inlineformset_factory(DiamondPiceBreak, DiamondPice, form=DiamondPiceForm, extra=5, max_num=5, can_delete=True,)



