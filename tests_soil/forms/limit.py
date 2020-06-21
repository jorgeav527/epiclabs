from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_soil.models import Limit, Liquid, Platic
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class LimitForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = Limit
        fields = [
            'pit',
            'layer',
            'extraction_data',
            'done_data',
            'course'
        ]
        labels = {
            'pit': 'Calicata',
            'layer': 'Estrato',
            'extraction_data': 'Fecha de Extracción',
            'done_data': 'Fecha del Ensayo',
        }
        help_texts = {
            'pit': 'Nombre Propio de la Calicata',
        }
        widgets = {
            'extraction_data': DateInput(),
            'done_data': DateInput(), 
        }


class LimitFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)

    class Meta:
        model = Limit
        fields = [
            'user',
            'pit',
            'layer',
            'extraction_data',
            'done_data',
            'reference_person',
            'construction',
        ]
        labels = {
            'pit': 'Calicata',
            'layer': 'Estrato',
            'extraction_data': 'Fecha de Extracción',
            'done_data': 'Fecha del Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'pit': 'Nombre Propio de la Calicata',
        }
        widgets = {
            'extraction_data': DateInput(),
            'done_data': DateInput(), 
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


class LiquidForm(forms.ModelForm):

    class Meta:
        model = Liquid
        fields = [
            'bowl',
            'hit',
            'bowl_weight',
            'wet_weight',
            'dry_weight',
        ]
        labels = {
            'bowl': 'Recipiente Numero',
            'hit': 'Numero de Golpes',
            'bowl_weight': 'Peso del Recipiente',
            'wet_weight': 'Peso Humedo de la Muestra',
            'dry_weight': 'Peso Seco de la Muestra',
        }
        help_texts = {
            'bowl_weight': 'Unidades (Gramos) <br> Aproximación (0.01 g)',
            'wet_weight': 'Unidades (Gramos) <br> Aproximación (0.01 g)',
            'dry_weight': 'Unidades (Gramos) <br> Aproximación (0.01 g)',
        }

LiquidFormSet = inlineformset_factory(Limit, Liquid, form=LiquidForm, max_num=3)


class PlasticForm(forms.ModelForm):

    class Meta:
        model = Platic
        fields = [
            'bowl',
            'bowl_weight',
            'wet_weight',
            'dry_weight',
        ]
        labels = {
            'bowl': 'Recipiente Numero',
            'bowl_weight': 'Peso del Recipiente',
            'wet_weight': 'Peso Humedo de la Muestra',
            'dry_weight': 'Peso Seco de la Muestra',
        }
        help_texts = {
            'bowl_weight': 'Unidades (Gramos) <br> Aproximación (0.01 g)',
            'wet_weight': 'Unidades (Gramos) <br> Aproximación (0.01 g)',
            'dry_weight': 'Unidades (Gramos) <br> Aproximación (0.01 g)',
        }

PlasticFormSet = inlineformset_factory(Limit, Platic, form=PlasticForm, max_num=3)