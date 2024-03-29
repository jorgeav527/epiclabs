from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_soil.models import ProctorM, DensityWetDry, Correction
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class ProctorMForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = ProctorM
        fields = [
            'material',
            'quarry',
            'process',
            'saturation_check',
            'gs',
            'correction_check',
            'sampling_date',
            'done_date',
            'course'
        ]
        labels = {
            'material': 'Material',
            'quarry': 'Cantera',
            'process': 'Tipo de Procedimiento',
            'saturation_check': 'Curva de 100% de Saturación',
            'gs': 'Gravedad Específica',
            'correction_check': 'Corrección',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
        }
        help_texts = {
            'material': 'Tipo de Material',
            'quarry': 'Nombre Propio de la Cantera',
            'gs': 'Dimensional',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class ProctorMFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)

    class Meta:
        model = ProctorM
        fields = [
            'user',
            'material',
            'quarry',
            'sampling_date',
            'process',
            'saturation_check',
            'gs',
            'correction_check',
            'done_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'material': 'Material',
            'quarry': 'Cantera',
            'process': 'Tipo de Procedimiento',
            'saturation_check': 'Curva de 100% de Saturación',
            'gs': 'Gravedad Específica',
            'correction_check': 'Corrección',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha del Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'material': 'Tipo de Material',
            'quarry': 'Nombre Propio de la Cantera',
            'gs': 'Dimensional',
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


class DensityWetDryForm(forms.ModelForm):

    class Meta:
        model = DensityWetDry
        fields = [
            'layers',
            'hits',
            'material_weight_P',
            'bowl_weight_P',
            'bowl_volume_P',
            'bowl',
            'bowl_weight',
            'wet_weight',
            'dry_weight',
        ]
        labels = {
            'layers': 'Nº de Capas',
            'hits': 'Nº de Golpes',
            'material_weight_P': 'Peso del suelo + molde',
            'bowl_weight_P': 'Peso del molde',
            'bowl_volume_P': 'Volumen del molde',
            'bowl': 'Recipiente Nº',
            'bowl_weight': 'Peso del recipiente',
            'wet_weight': 'Peso del material húmedo + recipiente',
            'dry_weight': 'Peso de material seco + recipiente',
        }
        help_texts = {
            'layers': 'Aproximación de 1',
            'hits': 'Aproximación de 1',
            'material_weight_P': 'Unidades (Gramos) <br> Aproximación (1 g)',
            'bowl_weight_P': 'Unidades (Gramos) <br> Aproximación (1 g)',
            'bowl_volume_P': 'Unidades (cm³) <br> Aproximación (0.1 cm³)',
            'bowl_weight': 'Unidades (Gramos) <br> Aproximación (1 g)',
            'wet_weight': 'Unidades (Gramos) <br> Aproximación (1 g)',
            'dry_weight': 'Unidades (Gramos) <br> Aproximación (1 g)',
        }

DensityWetDryFormSet = inlineformset_factory(ProctorM, DensityWetDry, form=DensityWetDryForm, max_num=5, extra=5)


# class SaturationForm(forms.ModelForm):

#     class Meta:
#         model = Saturation
#         fields = [
#             'frac_extrad_weight',
#             'frac_gruesa_weight',
#             'frac_fina_weight',  
#             'p_sp_frac_extrad',  
#             'p_sp_frac_gruesa',  
#             'g_sp_frac_fina',    
#         ]
#         labels = {
#             'frac_extrad_weight': '% en peso de fracción extradim',
#             'frac_gruesa_weight': '% en peso de fracción gruesa',
#             'frac_fina_weight': '% en peso de fracción fina',  
#             'p_sp_frac_extrad': 'P.Esp. aparente de la fracción extrad. a 20°c',  
#             'p_sp_frac_gruesa': 'P.Esp. aparente de la fracción gruesa a 20°c',  
#             'g_sp_frac_fina': 'G.Esp. específica de la fracción fina a 20°c',    
#         }
#         help_texts = {
#             'frac_extrad_weight': 'Unidades (%) <br> Aproximación (0.01%)',
#             'frac_gruesa_weight': 'Unidades (%) <br> Aproximación (0.01%)',
#             'frac_fina_weight': 'Unidades (%) <br> Aproximación (0.01%)',  
#             'p_sp_frac_extrad': 'Unidades (g/cm³) <br> Aproximación (0.001 g/cm³)',  
#             'p_sp_frac_gruesa': 'Unidades (g/cm³) <br> Aproximación (0.001 g/cm³)',  
#             'g_sp_frac_fina': 'Adimensional <br> Aproximación (0.001)',    
#         }

# SaturationFormSet = inlineformset_factory(ProctorM, Saturation, form=SaturationForm, max_num=1, can_delete=False)


class CorrectionForm(forms.ModelForm):

    class Meta:
        model = Correction
        fields = [
            'bowl_weight',
            'wet_weight',
            'dry_weight',  
        ]
        labels = {
            'bowl_weight': 'Peso del recipiente',
            'wet_weight': 'Peso de fracción extrad. húmeda + recipiente',
            'dry_weight': 'Peso de fracción extrad. seca + recipiente',  
        }
        help_texts = {
            'bowl_weight': 'Unidades (gramos) <br> Aproximación (0.1 g)',
            'wet_weight': 'Unidades (gramos) <br> Aproximación (0.1 g)',
            'dry_weight': 'Unidades (gramos) <br> Aproximación (0.1 g)', 
        }

CorrectionFormSet = inlineformset_factory(ProctorM, Correction, form=CorrectionForm, max_num=1, can_delete=False)
