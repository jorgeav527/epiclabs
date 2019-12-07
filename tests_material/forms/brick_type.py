from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_material.models import BrickType, VariationDimensions, Warping, DensityVoids, Suction, AbsSatuCoeff, CompretionBrick 
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class BrickTypeForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = BrickType
        fields = [
            'name_element',
            'brick_company',
            'n_d_length',
            'n_d_width',
            'n_d_high',
            'sampling_date',
            'done_date',
            'course',
        ]
        labels = {
            'name_element': 'Nombre del Elemento',
            'brick_company': 'Compañia de Ladrillos',
            'n_d_length': 'Dimención Nominal Largo',
            'n_d_width': 'Dimención Nominal Ancho',
            'n_d_high': 'Dimención Nominal Alto',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha de Ensayo',
        }
        help_texts = {
            'name_element': 'Nombre Propio',
            'n_d_length': 'Unidades (mm)',
            'n_d_width': 'Unidades (mm)',
            'n_d_high': 'Unidades (mm)',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class BrickTypeFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoje el Cliente", required=True)

    class Meta:
        model = BrickType
        fields = [
            'user',
            'name_element',
            'brick_company',
            'n_d_length',
            'n_d_width',
            'n_d_high',
            'sampling_date',
            'done_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'name_element': 'Nombre del Elemento',
            'brick_company': 'Compañia de Ladrillos',
            'n_d_length': 'Dimención Nominal Largo',
            'n_d_width': 'Dimención Nominal Ancho',
            'n_d_high': 'Dimención Nominal Alto',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha de Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'name_element': 'Nombre Propio',
            'n_d_length': 'Unidades (mm)',
            'n_d_width': 'Unidades (mm)',
            'n_d_high': 'Unidades (mm)',
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


class VadriationDimensionsForm(forms.ModelForm):

    class Meta:
        model = VariationDimensions
        fields = [
            'upface_length',
            'downface_length',
            'upface_width',
            'downface_width',
            'high_backside',
            'high_rightside',
            'high_frontside',
            'high_lefside',
        ]
        labels = {
            'upface_length': 'Largo Cara Superior',
            'downface_length': 'Largo Cara Inferior',
            'upface_width': 'Ancho Cara Superior',
            'downface_width': 'Ancho Cara Inferior',
            'high_backside': 'Alto Arista Posterior',
            'high_rightside': 'Alto Arista Derecha',
            'high_frontside': 'Alto Arista Delantera',
            'high_lefside': 'Alto Arista Izquierda',
        }
        help_texts = {
            'upface_length': 'Unidades (mm)',
            'downface_length': 'Unidades (mm)',
            'upface_width': 'Unidades (mm)',
            'downface_width': 'Unidades (mm)',
            'high_backside': 'Unidades (mm)',
            'high_rightside': 'Unidades (mm)',
            'high_frontside': 'Unidades (mm)',
            'high_lefside': 'Unidades (mm)',
        }

VadriationDimensionsFormSet = inlineformset_factory(BrickType, VariationDimensions, form=VadriationDimensionsForm, extra=5, max_num=5,)


class WarpingForm(forms.ModelForm):

    class Meta:
        model = Warping
        fields = [
            'upface_concave',
            'upface_convex',
            'downface_concave',
            'downface_convex',        
        ]
        labels = {
            'upface_concave': 'Cara Superior Concavo',
            'upface_convex': 'Cara Superior Convexo',
            'downface_concave': 'Cara Inferior Concavo',
            'downface_convex': 'Cara Inferior Convexo',
        }
        help_texts = {
            'upface_concave': 'Unidades (mm)',
            'upface_convex': 'Unidades (mm)',
            'downface_concave': 'Unidades (mm)',
            'downface_convex': 'Unidades (mm)',
        }

WarpingFormSet = inlineformset_factory(BrickType, Warping, form=WarpingForm, extra=5, max_num=5,)


class DensityVoidsForm(forms.ModelForm):

    class Meta:
        model = DensityVoids
        fields = [
            'length',
            'width',
            'high',
            'bar_500',
            'sc',
            'su',
            'bar',
            'weight',
        ]
        labels = {
            'length': 'Largo',
            'width': 'Ancho',
            'high': 'Alto',
            'bar_500': 'Peso de la Arena',
            'sc': 'Peso de 500ml de arena contenida en el cilindro graduado (Sc)',
            'su': 'Peso de la arena contenido en el espécimen de ensayo (Su)',
            'bar': 'Variable Comun',
            'weight': 'Peso del Especimen',
        }
        help_texts = {
            'length': 'Unidades (cm)',
            'width': 'Unidades (cm)',
            'high': 'Unidades (cm)',
            'bar_500': 'Unidades (ml)',
            'sc': 'Unidades (gr)',
            'su': 'Unidades (gr)',
            'bar': 'Adimncional',
            'weight': 'Unidades (gr)',
        }

DensityVoidsFormSet = inlineformset_factory(BrickType, DensityVoids, form=DensityVoidsForm, extra=5 ,max_num=5)


class SuctionForm(forms.ModelForm):

    class Meta:
        model = Suction
        fields = [
            'nomal_weight', 
            'dry_weight', 
            'length', 
            'width', 
            'bar_200', 
            'face_wet_weight', 
        ]
        labels = {
            'nomal_weight': 'Peso Inicial Normal', 
            'dry_weight': 'Peso Seco', 
            'length': 'Largo', 
            'width': 'Ancho', 
            'bar_200': 'Variable 200cm', 
            'face_wet_weight': 'Peso con la Cara Inferior Mojada', 
        }
        help_texts = {
            'nomal_weight': 'Unidades (gr)', 
            'dry_weight': 'Unidades (gr)', 
            'length': 'Unidades (cm)', 
            'width': 'Unidades (cm)', 
            'bar_200': 'Unidades (cm)', 
            'face_wet_weight': 'Unidades (gr/min)', 
        }

SuctionFormSet = inlineformset_factory(BrickType, Suction, form=SuctionForm, extra=5, max_num=5)


class AbsSatuCoeffForm(forms.ModelForm):

    class Meta:
        model = AbsSatuCoeff
        fields = [
            'dry_weight',
            'wet_weight_cool_24',
            'wet_weight_hot_24',
            'wet_weight_hot_5',
        ]
        labels = {
            'dry_weight': 'Peso Seco del Especímen',
            'wet_weight_cool_24': 'Peso del Especimen Saturado en Agua Fria a 24 Horas',
            'wet_weight_hot_24': 'Peso del Especimen Saturado en Agua Caliente a 24 Horas',
            'wet_weight_hot_5': 'Peso del Especimen Saturado en Agua Caliente a 5 Horas',
        }
        help_texts = {
            'dry_weight': 'Unidades (gr)',
            'wet_weight_cool_24': 'Unidades (gr)',
            'wet_weight_hot_24': 'Unidades (gr)',
            'wet_weight_hot_5': 'Unidades (gr)',
        }

AbsSatuCoeffFormSet = inlineformset_factory(BrickType, AbsSatuCoeff, form=AbsSatuCoeffForm, extra=5, max_num=5)


class CompretionBrickForm(forms.ModelForm):

    class Meta:
        model = CompretionBrick
        fields = [
            'upface_length',
            'upface_width',
            'downface_length',
            'downface_width',
            'load',
        ]
        labels = {
            'upface_length': 'Largo Superior',
            'upface_width': 'Ancho Superior',
            'downface_length': 'Largo Inferior',
            'downface_width': 'Ancho Inferior',
            'load': 'Carga',
        }
        help_texts = {
            'upface_length': 'Unidades (cm)',
            'upface_width': 'Unidades (cm)',
            'downface_length': 'Unidades (cm)',
            'downface_width': 'Unidades (cm)',
            'load': 'Unidades (kgf)',
        }

CompretionBrickFormSet = inlineformset_factory(BrickType, CompretionBrick, form=CompretionBrickForm, max_num=3)
