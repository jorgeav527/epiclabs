from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_soil.models import SpecificGravity, FractionPass, FractionRetained
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class SpecificGravityForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = SpecificGravity
        fields = [
            'material',
            'quarry',
            'sampling_date',
            'done_date',
            'course'
        ]
        labels = {
            'material': 'Material',
            'quarry': 'Cantera',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
        }
        help_texts = {
            'material': 'Tipo de Material',
            'quarry': 'Nombre Propio de la Cantera',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class SpecificGravityFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoje el Cliente", required=True)

    class Meta:
        model = SpecificGravity
        fields = [
            'user',
            'material',
            'quarry',
            'sampling_date',
            'done_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'material': 'Material',
            'quarry': 'Cantera',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'material': 'Tipo de Material',
            'quarry': 'Nombre Propio de la Cantera',
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


class FractionPassForm(forms.ModelForm):

    class Meta:
        model = FractionPass
        fields = [
            'material_pass',
            'temperature',
            'water_density',
            'pycnometer_volume',
            'pycnometer_mass',
            'sample_mass',    
            'mass_pyc_w_sample',
            'mass_bowl',
            'mass_bowl_sample',
            'coefficient_water',
        ]
        labels = {
            'material_pass': 'Fracción de suelo pasante en malla Nro. 4',
            'temperature': 'Temperatura de ensayo',
            'water_density': 'Densidad del agua a la temperatura de ensayo',
            'pycnometer_volume': 'Volumen promedio calibrado del picnómetro seco',
            'pycnometer_mass': 'Masa promedio calibrada del picnómetro seco',
            'sample_mass': 'Masa de la muestra de sólidos del suelo',    
            'mass_pyc_w_sample': 'Masa del picnómetro, agua y sólidos',
            'mass_bowl': 'Masa del recipiente para secado',
            'mass_bowl_sample': 'Masa del recipiente para secado + suelo seco',
            'coefficient_water': 'Coeficiente de temperatura del agua a 20°c',
        }
        help_texts = {
            'material_pass': 'Unidades (%)',
            'temperature': 'Unidades (°c)',
            'water_density': 'Unidades (g/mL)',
            'pycnometer_volume': 'Unidades (mL)',
            'pycnometer_mass': 'Unidades (gramos)',
            'sample_mass': 'Unidades (gramos)',    
            'mass_pyc_w_sample': 'Unidades (gramos)',
            'mass_bowl': 'Unidades (gramos)',
            'mass_bowl_sample': 'Unidades (gramos)',
            'coefficient_water': 'Adimencional',
        }

FractionPassFormSet = inlineformset_factory(SpecificGravity, FractionPass, form=FractionPassForm, extra=2 , max_num=2)


class FractionRetainedForm(forms.ModelForm):

    class Meta:
        model = FractionRetained
        fields = [
            'material_retained',
            'temperature_23',
            'saturated_sample',
            'w_basket_water',
            'w_basket_water_sample',
            'w_bowl',
            'w_bowl_sample',
            'coefficient_water',
        ]
        labels = {
            'material_retained': 'Fracción de suelo retenida en malla Nro. 4',
            'temperature_23': 'Temperatura de ensayo entre 23±1.7 °c',
            'saturated_sample': 'Peso de la muestra saturada con superficie seca en el aire',
            'w_basket_water': 'Peso de la canastilla dentro del agua',
            'w_basket_water_sample': 'Peso de la muestra saturada superficialmente seca + peso canastilla en agua',
            'w_bowl': 'Peso del recipiente para secado',
            'w_bowl_sample': 'Peso del recipiente + muestra seca al horno, 110°c',
            'coefficient_water': 'Coeficiente de temperatura del agua',
        }
        help_texts = {
            'material_retained': 'Unidades (%)',
            'temperature_23': 'Unidades (°c)' ,
            'saturated_sample': 'Unidades (gramos)',
            'w_basket_water': 'Unidades (gramos)',
            'w_basket_water_sample': 'Unidades (gramos)',
            'w_bowl': 'Unidades (gramos)',
            'w_bowl_sample': 'Unidades (gramos)',
            'coefficient_water': 'Unidades (gramos)',
        }

FractionRetainedFormSet = inlineformset_factory(SpecificGravity, FractionRetained, form=FractionRetainedForm, extra=2 , max_num=2)
