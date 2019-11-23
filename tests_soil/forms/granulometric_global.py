from django import forms
from functools import partial
from datetime import datetime

from accounts.models import User
from tests_soil.models import GranulometricGlobal
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class GranulometricGlobalForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = GranulometricGlobal
        fields = [
            'quarry',
            'layer',
            'sampling_date',
            'done_date',
            'tamiz_1_1o2',
            'tamiz_1',
            'tamiz_3o4',
            'tamiz_1o2',
            'tamiz_3o8',
            'tamiz_4',
            'tamiz_10',
            'tamiz_20',
            'tamiz_40',
            'tamiz_60',
            'tamiz_100',
            'tamiz_200',
            'tamiz_fondo',
            'course'
        ]
        labels = {
            'quarry': 'Cantera',
            'layer': 'Estrato',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'tamiz_1_1o2': 'Tamiz 1 1/2"',
            'tamiz_1': 'Tamiz 1"',
            'tamiz_3o4': 'Tamiz 3/4"',
            'tamiz_1o2': 'Tamiz 1/2"',
            'tamiz_3o8': 'Tamiz 3/8"',
            'tamiz_4': 'Tamiz Nº 4',
            'tamiz_10': 'Tamiz Nº 10',
            'tamiz_20': 'Tamiz Nº 20',
            'tamiz_40': 'Tamiz Nº 40',
            'tamiz_60': 'Tamiz Nº 60',
            'tamiz_100': 'Tamiz Nº 100',
            'tamiz_200': 'Tamiz Nº 200',
            'tamiz_fondo': 'Tamiz de Fondo',
        }
        help_texts = {
            'quarry': 'Nombre propio de la Cantera',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'tamiz_1_1o2': 'Unidades (gramos)',
            'tamiz_1': 'Unidades (gramos)',
            'tamiz_3o4': 'Unidades (gramos)',
            'tamiz_1o2': 'Unidades (gramos)',
            'tamiz_3o8': 'Unidades (gramos)',
            'tamiz_4': 'Unidades (gramos)',
            'tamiz_10': 'Unidades (gramos)',
            'tamiz_20': 'Unidades (gramos)',
            'tamiz_40': 'Unidades (gramos)',
            'tamiz_60': 'Unidades (gramos)',
            'tamiz_100': 'Unidades (gramos)',
            'tamiz_200': 'Unidades (gramos)',
            'tamiz_fondo': 'Unidades (gramos)',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class GranulometricGlobalFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoje el Cliente", required=True)

    class Meta:
        model = GranulometricGlobal
        fields = [
            'user',
            'quarry',
            'layer',
            'sampling_date',
            'done_date',
            'tamiz_1_1o2',
            'tamiz_1',
            'tamiz_3o4',
            'tamiz_1o2',
            'tamiz_3o8',
            'tamiz_4',
            'tamiz_10',
            'tamiz_20',
            'tamiz_40',
            'tamiz_60',
            'tamiz_100',
            'tamiz_200',
            'tamiz_fondo',
            'reference_person',
            'construction',
        ]
        labels = {
            'quarry': 'Cantera',
            'layer': 'Estrato',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'tamiz_1_1o2': 'Tamiz 1 1/2"',
            'tamiz_1': 'Tamiz 1"',
            'tamiz_3o4': 'Tamiz 3/4"',
            'tamiz_1o2': 'Tamiz 1/2"',
            'tamiz_3o8': 'Tamiz 3/8"',
            'tamiz_4': 'Tamiz Nº 4',
            'tamiz_10': 'Tamiz Nº 10',
            'tamiz_20': 'Tamiz Nº 20',
            'tamiz_40': 'Tamiz Nº 40',
            'tamiz_60': 'Tamiz Nº 60',
            'tamiz_100': 'Tamiz Nº 100',
            'tamiz_200': 'Tamiz Nº 200',
            'tamiz_fondo': 'Tamiz de Fondo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'quarry': 'Nombre propio de la Cantera',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'tamiz_1_1o2': 'Unidades (gramos)',
            'tamiz_1': 'Unidades (gramos)',
            'tamiz_3o4': 'Unidades (gramos)',
            'tamiz_1o2': 'Unidades (gramos)',
            'tamiz_3o8': 'Unidades (gramos)',
            'tamiz_4': 'Unidades (gramos)',
            'tamiz_10': 'Unidades (gramos)',
            'tamiz_20': 'Unidades (gramos)',
            'tamiz_40': 'Unidades (gramos)',
            'tamiz_60': 'Unidades (gramos)',
            'tamiz_100': 'Unidades (gramos)',
            'tamiz_200': 'Unidades (gramos)',
            'tamiz_fondo': 'Unidades (gramos)',
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


