from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_soil.models import SandCone, HumidDensity, ContentMoisture, CorrectionSandCone
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class SandConeForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = SandCone
        fields = [
            'sampling_name',
            'progressive_sector',
            'section_level',
            'element_side',
            'layer',
            'moisture',
            'weight_dry_max',
            'opt_moisture',
            'sampling_date',
            'done_date',
            'course',
        ]
        labels = {
            'sampling_name': 'Muestra',
            'progressive_sector': 'Sector o Progresiva',
            'section_level': 'Tramo o Nivel',
            'element_side': 'Elemento o Lado',
            'layer': 'Capa',
            'moisture': 'Corrección?',
            'weight_dry_max': 'Peso unit. Seco máx.',
            'opt_moisture': 'Ópt. Cont. de humedad' ,
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
        }
        help_texts = {
            'weight_dry_max': 'Unidades (g/cm³) <br> Aproximación (0.01 g/cm³)',
            'opt_moisture': 'Unidades (%) <br> Aproximación (0.1%)',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class SandConeFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)

    class Meta:
        model = SandCone
        fields = [
            'user',
            'sampling_name',
            'progressive_sector',
            'section_level',
            'element_side',
            'layer',
            'moisture',
            'weight_dry_max',
            'opt_moisture',
            'sampling_date',
            'done_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'sampling_name': 'Muestra',
            'progressive_sector': 'Sector o Progresiva',
            'section_level': 'Tramo o Nivel',
            'element_side': 'Elemento o Lado',
            'layer': 'Capa',
            'moisture': 'Corrección?',
            'weight_dry_max': 'Peso unit. Seco máx.',
            'opt_moisture': 'Ópt. Cont. de humedad',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'weight_dry_max': 'Unidades (g/cm³) <br> Aproximación (0.01 g/cm³)',
            'opt_moisture': 'Unidades (%) <br> Aproximación (0.1%)',
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


class HumidDensityForm(forms.ModelForm):

    class Meta:
        model = HumidDensity
        fields = [
            'bowl_weight_sand',
            'bowl_weight_remaining_sand',
            'weight_sand_cone_plate',
            'sand_density',
            'sample_weight_container',
            'container_weight',
        ]
        labels = {
            'bowl_weight_sand': 'Peso del frasco + arena',
            'bowl_weight_remaining_sand': 'Peso del frasco + arena que queda',
            'weight_sand_cone_plate': 'Peso de arena en el cono y placa',
            'sand_density': 'Densidad de la arena',
            'sample_weight_container': 'Peso muestra total + recipiente',
            'container_weight': 'Peso de recipiente',
        }
        help_texts = {
            'bowl_weight_sand': 'Unidades (g) <br> Aproximación (1 g)',
            'bowl_weight_remaining_sand': 'Unidades (g) <br> Aproximación (1 g)',
            'weight_sand_cone_plate': 'Unidades (g) <br> Aproximación (1 g)',
            'sand_density': 'Unidades (g/cm³) <br> Aproximación (0.01 g/cm³)',
            'sample_weight_container': 'Unidades (g) <br> Aproximación (1 g)',
            'container_weight': 'Unidades (g) <br> Aproximación (1 g)',
        }

HumidDensityFormSet = inlineformset_factory(SandCone, HumidDensity, form=HumidDensityForm, max_num=1, can_delete=False,)


class ContentMoistureForm(forms.ModelForm):

    class Meta:
        model = ContentMoisture
        fields = [
            'sample_fraction_pass',
            'bowl_weight',
            'wet_sample_weight_bowl',
            'dry_sample_weight_bowl',
        ]
        labels = {
            'sample_fraction_pass': 'Fracción de muestra',
            'bowl_weight': 'Peso de recipiente',
            'wet_sample_weight_bowl': 'Peso de muestra húmeda + recipiente',
            'dry_sample_weight_bowl': 'Peso de muestra seca + recipiente',
        }
        help_texts = {
            'bowl_weight': 'Unidades (g) <br> Aproximación (0.1 g)',
            'wet_sample_weight_bowl': 'Unidades (g) <br> Aproximación (0.1 g)',
            'dry_sample_weight_bowl': 'Unidades (g) <br> Aproximación (0.1 g)',
        }

ContentMoistureFormSet = inlineformset_factory(SandCone, ContentMoisture, form=ContentMoistureForm, max_num=1, can_delete=False,)


class CorrectionSandConeForm(forms.ModelForm):

    class Meta:
        model = CorrectionSandCone
        fields = [
            'wet_fraction_weight',
            'p_e_ap_frac_extrad',
            'per_abs_tails_extrad',
        ]
        labels = {
            'wet_fraction_weight': 'Peso de fracción extradimensionada húmeda',
            'p_e_ap_frac_extrad': 'P.E Ap. Frac. Extrad. A 20°c',
            'per_abs_tails_extrad': '% Abs. Frac. Extrad.',
        }
        help_texts = {
            'wet_fraction_weight': 'Unidades (g) <br> Aproximación (1 g)',
            'p_e_ap_frac_extrad': 'Unidades (g/cm³), NTP 400.021 - ASTM C127 <br> Aproximación (0.001g/cm³)',
            'per_abs_tails_extrad': 'Unidades (%), NTP 400.021 - ASTM C127 <br> Aproximación (0.1%)',
        }

CorrectionSandConeFormSet = inlineformset_factory(SandCone, CorrectionSandCone, form=CorrectionSandConeForm, max_num=1, can_delete=False,)