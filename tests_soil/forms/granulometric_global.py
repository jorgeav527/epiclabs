from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_soil.models import GranulometricGlobal, GlobalMesh
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
            'hygr_humid',
            'organic',
            'liquid_limit',
            'plastic_limit',
            'max_size',
            'course',
        ]
        labels = {
            'quarry': 'Cantera',
            'layer': 'Estrato',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'hygr_humid': '% humedad higroscópica de la fracción fina',
            'organic': 'Contenido de materia orgánica',
            'liquid_limit': 'Limite Líquido',
            'plastic_limit': 'Límite Plástico',
            'max_size': 'Tamaño máximo',
        }
        help_texts = {
            'quarry': 'Nombre propio de la Cantera',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'hygr_humid': 'Porcentaje',
            'liquid_limit': 'Porcentaje',
            'plastic_limit': 'Porcentaje',
            'max_size': 'Pulgadas',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class GranulometricGlobalFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)

    class Meta:
        model = GranulometricGlobal
        fields = [
            'user',
            'quarry',
            'layer',
            'sampling_date',
            'done_date',
            'hygr_humid',
            'organic',
            'liquid_limit',
            'plastic_limit',
            'max_size',
            'reference_person',
            'construction',
        ]
        labels = {
            'quarry': 'Cantera',
            'layer': 'Estrato',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'hygr_humid': '% humedad higroscópica de la fracción fina',
            'organic': 'Contenido de materia orgánica',
            'liquid_limit': 'Limite Líquido',
            'plastic_limit': 'Límite Plástico',
            'max_size': 'Tamaño máximo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'quarry': 'Nombre propio de la Cantera',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'hygr_humid': 'Porcentaje',
            'liquid_limit': 'Porcentaje',
            'plastic_limit': 'Porcentaje',
            'max_size': 'Pulgadas',
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


class GlobalMeshForm(forms.ModelForm):

    class Meta:
        model = GlobalMesh
        fields = [
            'tamiz_4',
            'tamiz_3',
            'tamiz_2_1o2',
            'tamiz_2',
            'tamiz_1_1o2',
            'tamiz_1',
            'tamiz_3o4',
            'tamiz_1o2',
            'tamiz_3o8',
            'tamiz_N_4',
            'tamiz_N_8',
            'tamiz_N_10',
            'tamiz_N_16',
            'tamiz_N_20',
            'tamiz_N_30',
            'tamiz_N_40',
            'tamiz_N_50',
            'tamiz_N_60',
            'tamiz_N_80',
            'tamiz_N_100',
            'tamiz_N_140',
            'tamiz_N_200',
            'tamiz_fondo',
        ]
        labels = {
            'tamiz_4': 'Tamiz 4 inch',
            'tamiz_3': 'Tamiz 3 inch',
            'tamiz_2_1o2': 'Tamiz 2 1/2 inch',
            'tamiz_2': 'Tamiz 2 inch',
            'tamiz_1_1o2': 'Tamiz 1 1/2 inch',
            'tamiz_1': 'Tamiz 1 inch',
            'tamiz_3o4': 'Tamiz 3/4 inch',
            'tamiz_1o2': 'Tamiz 1/2 inch',
            'tamiz_3o8': 'Tamiz 3/8 inch',
            'tamiz_N_4': 'Tamiz Nº 4',
            'tamiz_N_8': 'Tamiz Nº 8',
            'tamiz_N_10': 'Tamiz Nº 10',
            'tamiz_N_16': 'Tamiz Nº 16',
            'tamiz_N_20': 'Tamiz Nº 20',
            'tamiz_N_30': 'Tamiz Nº 30',
            'tamiz_N_40': 'Tamiz Nº 40',
            'tamiz_N_50': 'Tamiz Nº 50',
            'tamiz_N_60': 'Tamiz Nº 60',
            'tamiz_N_80': 'Tamiz Nº 80',
            'tamiz_N_100': 'Tamiz Nº 100',
            'tamiz_N_140': 'Tamiz Nº 140',
            'tamiz_N_200': 'Tamiz Nº 200',
            'tamiz_fondo': 'Tamiz fondo',
        }
        help_texts = {
            'tamiz_4': 'Unidades (gramos)',
            'tamiz_3': 'Unidades (gramos)',
            'tamiz_2_1o2': 'Unidades (gramos)',
            'tamiz_2': 'Unidades (gramos)',
            'tamiz_1_1o2': 'Unidades (gramos)',
            'tamiz_1': 'Unidades (gramos)',
            'tamiz_3o4': 'Unidades (gramos)',
            'tamiz_1o2': 'Unidades (gramos)',
            'tamiz_3o8': 'Unidades (gramos)',
            'tamiz_N_4': 'Unidades (gramos)',
            'tamiz_N_8': 'Unidades (gramos)',
            'tamiz_N_10': 'Unidades (gramos)',
            'tamiz_N_16': 'Unidades (gramos)',
            'tamiz_N_20': 'Unidades (gramos)',
            'tamiz_N_30': 'Unidades (gramos)',
            'tamiz_N_40': 'Unidades (gramos)',
            'tamiz_N_50': 'Unidades (gramos)',
            'tamiz_N_60': 'Unidades (gramos)',
            'tamiz_N_80': 'Unidades (gramos)',
            'tamiz_N_100': 'Unidades (gramos)',
            'tamiz_N_140': 'Unidades (gramos)',
            'tamiz_N_200': 'Unidades (gramos)',
            'tamiz_fondo': 'Unidades (gramos)',
        }

GlobalMeshFormSet = inlineformset_factory(GranulometricGlobal, GlobalMesh, form=GlobalMeshForm, max_num=1, can_delete=False,)
