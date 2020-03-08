from django import forms
from functools import partial
from datetime import datetime
from django.forms import inlineformset_factory


from accounts.models import User
from tests_concrete.models import PrismBreak, Prism
from construction.models import Construction
from reference_person.models import ReferencePerson
from course.models import Course

DateInput = partial(forms.DateInput, {"class": "datepicker"})

class PrismBreakForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Especifico", required=True)

    class Meta:
        model = PrismBreak 
        fields = [
            'prism_type',
            'fc_esp',
            'course',
        ]
        labels = {
            'prism_type': 'Tipo de Prisma',
            'fc_esp': 'Resistencia de Diseño',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²)', 
        }


class PrismBreakFormClient(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_client=True), label="Escoge el Cliente", required=True)
    sampling_date = forms.DateField(required=True, label="Fecha de Muestreo", widget=DateInput(), initial=datetime.now)

    class Meta:
        model = PrismBreak 
        fields = [
            'user',
            'prism_type',
            'fc_esp',
            'sampling_date',
            'reference_person',
            'construction',
        ]
        labels = {
            'prism_type': 'Tipo de Prisma',
            'fc_esp': 'Resistencia de Diseño',
            'reference_person': 'Persona de Referencia',
            'construction': 'Construcción de Referencia',
        }
        help_texts = {
            'fc_esp': 'Unidades (kgf/cm²)', 
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

    
class PrismForm(forms.ModelForm):

    class Meta:
        model = Prism
        fields = [
            'poured_date',
            'break_date',
            'element_name',
            'D_1',
            'D_2',
            'load',
        ]
        labels = {
            'poured_date': 'Fecha de Vaciado',
            'break_date': 'Fecha de Rotura',
            'element': 'Elemento',    
            'D_1': 'Largo',
            'D_2': 'Ancho',
            'load': 'Carga',
        }
        help_texts = {
            'D_1': 'Unidades (cm)',
            'D_2': 'Unidades (cm)',
            'load': 'Unidades (kgf)',
        }
        widgets = {
            'poured_date': DateInput(),
            'break_date': DateInput(),
        }


PrismFormSet = inlineformset_factory(PrismBreak , Prism, form=PrismForm, extra=3, max_num=3, can_delete=True)
