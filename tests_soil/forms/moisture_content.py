from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_soil.models import MoistureContent, MoistureMaterial
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class MoistureContentForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = MoistureContent
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


class MoistureContentFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)

    class Meta:
        model = MoistureContent
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


class MoistureMaterialForm(forms.ModelForm):

    class Meta:
        model = MoistureMaterial
        fields = [
            'material',
            'bowl_weight',
            'wet_weight',
            'dry_weight',  
        ]
        labels = {
            'material': 'Material',
            'bowl_weight': 'Peso del recipiente',
            'wet_weight': 'Peso de fracción extrad. húmeda + recipiente',
            'dry_weight': 'Peso de fracción extrad. seca + recipiente',  
        }
        help_texts = {
            'bowl_weight': 'Unidades (gramos) <br> Aproximación (0.1 g)',
            'wet_weight': 'Unidades (gramos) <br> Aproximación (0.1 g)',
            'dry_weight': 'Unidades (gramos) <br> Aproximación (0.1 g)', 
        }

MoistureMaterialFormSet = inlineformset_factory(MoistureContent, MoistureMaterial, form=MoistureMaterialForm, extra=6 , max_num=6)
