from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory

from accounts.models import User
from tests_material.models import MasonryCompression, Masonry
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class MasonryCompressionForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = MasonryCompression
        fields = [
            'brick_type',
            'element_name',
            'sampling_date',
            'done_date',
            'course',
        ]
        labels = {
            'brick_type': 'Tipo de Unidad',
            'sampling_date': 'Fecha de Muestreo',
            'element_name': 'Elemento Nombre',
            'done_date': 'Fecha de Ensayo',
        }
        help_texts = {
            'element_name': 'Nombre Propio',
        }
        widgets = {
            'sampling_date': DateInput(),
            'done_date': DateInput(),
        }


class MasonryCompressionFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)
    sampling_date = forms.DateField(required=True, label="Fecha de Muestreo", widget=DateInput(), initial=datetime.now)

    class Meta:
        model = MasonryCompression
        fields = [
            'user',
            'brick_type',
            'element_name',
            'sampling_date',
            'done_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'brick_type': 'Tipo de Unidad',
            'element_name': 'Elemento Nombre',
            'sampling_date': 'Fecha de Muestreo',
            'done_date': 'Fecha de Ensayo',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'name_element': 'Nombre Propio',
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


class MasonryForm(forms.ModelForm):

    class Meta:
        model = Masonry
        fields = [
            'poured_date',
            'break_date',
            'element_name',
            'L',
            'A',
            'hp',
            'load',
        ]
        labels = {
            'poured_date': 'Fecha de Vaciado',
            'break_date': 'Fecha de Rotura',
            'element_name': 'Elemento Nombre',
            'L': 'Longitud',
            'A': 'Ancho o Espesor de la Pila o Murete (tp)',
            'hp': 'Altura de la Pila o Murete (hp)',
            'load': 'Carga',
        }
        help_texts = {
            'poured_date': 'mm/dd/yyyy',
            'break_date': 'mm/dd/yyyy',
            'L': 'Unidades (mm) <br> Aproximación (1 mm)',
            'A': 'Unidades (mm) <br> Aproximación (1 mm)',
            'hp': 'Unidades (mm) <br> Aproximación (1 mm)',
            'load': 'Unidades (kgf) <br> Aproximación (1 kgf)',
        }
        widgets = {
            'poured_date': DateInput(),
            'break_date': DateInput(),
        }

MasonryFormSet = inlineformset_factory(MasonryCompression, Masonry, form=MasonryForm, extra=5, max_num=5, can_delete=True)