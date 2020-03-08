from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_soil.models import Equivalent, Equiv
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class EquivalentForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = Equivalent
        fields = [
            'pit',
            'layer',
            'sampling_date',
            'done_date',
            'course'
        ]
        labels = {
            'pit': 'Calicata',
            'layer': 'Estrato',
            'sampling_date': 'Fecha de Extracción',
            'done_date': 'Fecha del Ensayo',
        }
        help_texts = {
            'pit': 'Nombre Propio de la Calicata',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class EquivalentFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)

    class Meta:
        model = Equivalent
        fields = [
            'user',
            'pit',
            'layer',
            'sampling_date',
            'done_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'pit': 'Calicata',
            'layer': 'Estrato',
            'sampling_date': 'Fecha de Extracción',
            'done_date': 'Fecha del Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'pit': 'Nombre Propio de la Calicata',
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


class EquivForm(forms.ModelForm):

    class Meta:
        model = Equiv
        fields = [
            'max_size',
            'start_sat_time',
            'out_sat_time',
            'start_dec_time',
            'out_dec_time',
            'max_high_fine',
            'max_high_sand',
        ]
        labels = {
            'max_size': 'Tamaño Maximo',
            'start_sat_time': 'Hora de Entrada a Saturación',
            'out_sat_time': 'Hora de Salida de Saturación',
            'start_dec_time': 'Hora de Entrada a Decantación',
            'out_dec_time': 'Hora de Salida de Decantación',
            'max_high_fine': 'Altura Máxima del Material Fino',
            'max_high_sand': 'Altura Máxima de la Arena'
        }
        help_texts = {
            'max_size': 'Pasante del tamiz #4',
            'start_sat_time': 'Unidades (hh:mm:ss)',
            'out_sat_time': 'Unidades (hh:mm:ss)',
            'start_dec_time': 'Unidades (hh:mm:ss)',
            'out_dec_time': 'Unidades (hh:mm:ss)',
            'max_high_fine': 'Unidades (mm)',
            'max_high_sand': 'Unidades (mm)',
        }

EquivFormSet = inlineformset_factory(Equivalent, Equiv, form=EquivForm, max_num=3)
