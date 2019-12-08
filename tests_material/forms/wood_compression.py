from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_material.models import WoodCompression, ParallelPerpendicular 
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class WoodCompressionForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = WoodCompression
        fields = [
            'name_element',
            'wood_name',
            'sampling_date',
            'done_date',
            'course',
        ]
        labels = {
            'name_element': 'Elemento Nombre',
            'wood_name': 'Nombre de la Madera',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha de Ensayo',
        }
        help_texts = {
            'name_element': 'Nombre Propio',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class WoodCompressionFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoje el Cliente", required=True)

    class Meta:
        model = WoodCompression
        fields = [
            'user',
            'name_element',
            'wood_name',
            'sampling_date',
            'done_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'name_element': 'Elemento Nombre',
            'wood_name': 'Nombre de la Madera',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha de Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'name_element': 'Nombre Propio',
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


class ParallelPerpendicularForm(forms.ModelForm):

    class Meta:
        model = ParallelPerpendicular
        fields = [
            'type_compression',
            'length_1',
            'width_1',
            'length_2',
            'width_2',
            'load',
        ]
        labels = {
            'type_compression': 'Tipo de Compresión',
            'length_1': 'Largo Superior',
            'width_1': 'Ancho Superior',
            'length_2': 'Largo Inferior',
            'width_2': 'Ancho Inferior',
            'load': 'Carga',
        }
        help_texts = {
            'length_1': 'Unidades (cm)',
            'width_1': 'Unidades (cm)',
            'length_2': 'Unidades (cm)',
            'width_2': 'Unidades (cm)',
            'load': 'Unidades (kgf)',
        }

ParallelPerpendicularFormSet = inlineformset_factory(WoodCompression, ParallelPerpendicular, form=ParallelPerpendicularForm, extra=4 , max_num=4)