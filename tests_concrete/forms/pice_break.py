from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory


from accounts.models import User
from tests_concrete.models import PiceBreak, Pice
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class PiceBreakForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = PiceBreak
        fields = [
            'pice_type',
            'fc_esp',
            'course',
        ]
        labels = {
            'pice_type': 'Tipo de Probeta',
            'fc_esp': 'Resistencia de Diseño',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²)', 
        }


class PiceBreakFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)
    sampling_date = forms.DateField(required=True, label="Fecha de Muestreo", widget=DateInput(), initial=datetime.now)

    class Meta:
        model = PiceBreak
        fields = [
            'user',
            'pice_type',
            'fc_esp',
            'sampling_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'pice_type': 'Tipo de Probeta',
            'fc_esp': 'Resistencia de Diseño',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²)', 
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

    
class PiceForm(forms.ModelForm):

    class Meta:
        model = Pice
        fields = [
            'poured_date',
            'break_date',
            'element_name',
            'D_1',
            'D_2',
            'load',
        ]
        labels = {
            'poured_date': 'Fecha de Vaciado',
            'break_date': 'Fecha de Rotura',
            'element': 'Elemento',    
            'D_1': 'Diametro 1',
            'D_2': 'Diametro 2',
            'load': 'Carga',
        }
        help_texts = {
            'D_1': 'Unidades (pulgadas)',
            'D_2': 'Unidades (pulgadas)',
            'load': 'Unidades (kgf)',
        }
        widgets = {
            'poured_date': DateInput(),
            'break_date': DateInput(),
        }

PiceFormSet = inlineformset_factory(PiceBreak, Pice, form=PiceForm, extra=5, max_num=5, can_delete=True)
