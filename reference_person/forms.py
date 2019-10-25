from django import forms

from .models import ReferencePerson

class ReferencePersonForm(forms.ModelForm):
    TITLE_CHOICES = (
        ("NINGUNA", "Ninguna"),
        ("Ope", "Operario"),
        ("Tec", "Técnico"),
        ("Ing", "Ingeniero"),
        ("Arq", "Arquitecto"),
        ("Mg", "Magister"),
        ("Dr", "Doctor"),
    )

    title   = forms.ChoiceField(required=True, choices=TITLE_CHOICES, label='Formación', help_text='Selecciona la Formación',)
    name    = forms.CharField(required=True, label="Nombre Completo",)
    dni     = forms.IntegerField(required=True, label='DNI', help_text='Documento Nacional de Identidad',)
    phone   = forms.IntegerField(required=True, label='Telefono o Celular',)

    class Meta:
        model = ReferencePerson
        fields = ("title", "name", "dni", "phone",)