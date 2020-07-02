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
            'brick_company': 'Compañía de Ladrillos',
            'n_d_length': 'Dimensión Nominal Largo',
            'n_d_width': 'Dimensión Nominal Ancho',
            'n_d_high': 'Dimensión Nominal Alto',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha de Ensayo',
        }
        help_texts = {
            'n_d_length': 'Unidades (mm) <br> Aproximación (1 mm)',
            'n_d_width': 'Unidades (mm) <br> Aproximación (1 mm)',
            'n_d_high': 'Unidades (mm) <br> Aproximación (1 mm)',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(), 
        }


class BrickTypeFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)

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
            'brick_company': 'Compañía de Ladrillos',
            'n_d_length': 'Dimensión Nominal Largo',
            'n_d_width': 'Dimensión Nominal Ancho',
            'n_d_high': 'Dimensión Nominal Alto',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha de Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'n_d_length': 'Unidades (mm) <br> Aproximación (1 mm)',
            'n_d_width': 'Unidades (mm) <br> Aproximación (1 mm)',
            'n_d_high': 'Unidades (mm) <br> Aproximación (1 mm)',
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
            'name_element',
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
            'name_element': 'Nombre del Elemento',
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
            'upface_length': 'Unidades (mm) <br> Aproximación (1 mm)',
            'downface_length': 'Unidades (mm) <br> Aproximación (1 mm)',
            'upface_width': 'Unidades (mm) <br> Aproximación (1 mm)',
            'downface_width': 'Unidades (mm) <br> Aproximación (1 mm)',
            'high_backside': 'Unidades (mm) <br> Aproximación (1 mm)',
            'high_rightside': 'Unidades (mm) <br> Aproximación (1 mm)',
            'high_frontside': 'Unidades (mm) <br> Aproximación (1 mm)',
            'high_lefside': 'Unidades (mm) <br> Aproximación (1 mm)',
        }

VadriationDimensionsFormSet = inlineformset_factory(BrickType, VariationDimensions, form=VadriationDimensionsForm, extra=5, max_num=5, can_delete=True)


class WarpingForm(forms.ModelForm):

    class Meta:
        model = Warping
        fields = [
            'name_element',
            'upface_concave',
            'upface_convex',
            'downface_concave',
            'downface_convex',        
        ]
        labels = {
            'name_element': 'Nombre del Elemento',
            'upface_concave': 'Cara Superior Cóncavo',
            'upface_convex': 'Cara Superior Convexo',
            'downface_concave': 'Cara Inferior Cóncavo',
            'downface_convex': 'Cara Inferior Convexo',
        }
        help_texts = {
            'upface_concave': 'Unidades (mm) <br> Aproximación (1 mm)',
            'upface_convex': 'Unidades (mm) <br> Aproximación (1 mm)',
            'downface_concave': 'Unidades (mm) <br> Aproximación (1 mm)',
            'downface_convex': 'Unidades (mm) <br> Aproximación (1 mm)',
        }

WarpingFormSet = inlineformset_factory(BrickType, Warping, form=WarpingForm, extra=5, max_num=5, can_delete=True)


class DensityVoidsForm(forms.ModelForm):

    class Meta:
        model = DensityVoids
        fields = [
            'name_element',
            'length',
            'width',
            'high',
            'sc',
            'su',
            'weight',
        ]
        labels = {
            'name_element': 'Nombre del Elemento',
            'length': 'Largo',
            'width': 'Ancho',
            'high': 'Alto',
            'sc': 'Densidad de la arena calibrada',
            'su': 'Peso de la arena contenido en el espécimen de ensayo',
            'weight': 'Peso del Espécimen',
        }
        help_texts = {
            'length': 'Unidades (mm) <br> Aproximación (1 mm)',
            'width': 'Unidades (mm) <br> Aproximación (1 mm)',
            'high': 'Unidades (mm) <br> Aproximación (1 mm)',
            'sc': 'Unidades (gr/cm³) <br> Aproximación (0.01 gr/cm³)',
            'su': 'Unidades (gr) <br> Aproximación (0.5 gr)',
            'weight': 'Unidades (gr) <br> Aproximación (0.5 gr)',
        }

DensityVoidsFormSet = inlineformset_factory(BrickType, DensityVoids, form=DensityVoidsForm, extra=5 ,max_num=5, can_delete=True)


class SuctionForm(forms.ModelForm):

    class Meta:
        model = Suction
        fields = [
            'name_element',
            'nomal_weight', 
            'dry_weight', 
            'length', 
            'width', 
            'face_wet_weight', 
        ]
        labels = {
            'name_element': 'Nombre del Elemento',
            'nomal_weight': 'Peso Inicial Normal', 
            'dry_weight': 'Peso Seco', 
            'length': 'Largo', 
            'width': 'Ancho', 
            'face_wet_weight': 'Peso con la Cara Inferior Mojada', 
        }
        help_texts = {
            'nomal_weight': 'Unidades (gr) <br> Aproximación (0.5 gr)', 
            'dry_weight': 'Unidades (gr) <br> Aproximación (0.5 gr)', 
            'length': 'Unidades (mm) <br> Aproximación (1 mm)', 
            'width': 'Unidades (mm) <br> Aproximación (1 mm)', 
            'face_wet_weight': 'Unidades (gr/min/200cm²) <br> Aproximación (0.5 gr/min/200cm²)', 
        }

SuctionFormSet = inlineformset_factory(BrickType, Suction, form=SuctionForm, extra=5, max_num=5, can_delete=True)


class AbsSatuCoeffForm(forms.ModelForm):

    class Meta:
        model = AbsSatuCoeff
        fields = [
            'name_element',
            'dry_weight',
            'wet_weight_cool_24',
            'wet_weight_hot_5',
        ]
        labels = {
            'name_element': 'Nombre del Elemento',
            'dry_weight': 'Peso Seco del Espécimen',
            'wet_weight_cool_24': 'Peso del Espécimen Saturado en Agua Fría a 24 Horas',
            'wet_weight_hot_5': 'Peso del Espécimen Saturado en Agua Caliente a 5 Horas',
        }
        help_texts = {
            'dry_weight': 'Unidades (gr) <br> Aproximación (0.5 gr)',
            'wet_weight_cool_24': 'Unidades (gr) <br> Aproximación (0.5 gr)',
            'wet_weight_hot_5': 'Unidades (gr) <br> Aproximación (0.5 gr)',
        }

AbsSatuCoeffFormSet = inlineformset_factory(BrickType, AbsSatuCoeff, form=AbsSatuCoeffForm, extra=5, max_num=5, can_delete=True)


class CompretionBrickForm(forms.ModelForm):

    class Meta:
        model = CompretionBrick
        fields = [
            'name_element',
            'upface_length',
            'upface_width',
            'downface_length',
            'downface_width',
            'load',
        ]
        labels = {
            'name_element': 'Nombre del Elemento',
            'upface_length': 'Largo Superior',
            'upface_width': 'Ancho Superior',
            'downface_length': 'Largo Inferior',
            'downface_width': 'Ancho Inferior',
            'load': 'Carga',
        }
        help_texts = {
            'upface_length': 'Unidades (mm) <br> Aproximación (1 mm)',
            'upface_width': 'Unidades (mm) <br> Aproximación (1 mm)',
            'downface_length': 'Unidades (mm) <br> Aproximación (1 mm)',
            'downface_width': 'Unidades (mm) <br> Aproximación (1 mm)',
            'load': 'Unidades (kgf) <br> Aproximación (1 kgf)',
        }

CompretionBrickFormSet = inlineformset_factory(BrickType, CompretionBrick, form=CompretionBrickForm, extra=5, max_num=5, can_delete=True)
